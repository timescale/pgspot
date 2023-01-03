from pglast import ast, parse_sql, parse_plpgsql
from pglast.parser import ParseError
from pglast.stream import RawStream
from pglast.visitors import Visitor
from pglast.enums.parsenodes import VariableSetKind, TransactionStmtKind, ObjectType
from .formatters import (
    get_text,
    raw_sql,
    format_name,
    format_function,
    format_aggregate,
)
from .state import State
import re


def visit_sql(state, sql, searchpath_secure=False, toplevel=False):
    # We have to iterate over toplevel items ourselves cause the visitor does
    # breadth-first iteration, which would conflict with our search_path state
    # tracking.

    # @extschema@ is placeholder in extension scripts for
    # the schema the extension gets installed in
    sql = sql.replace("@extschema@", "extschema")
    sql = sql.replace("@extowner@", "extowner")
    sql = sql.replace("@database_owner@", "database_owner")
    # postgres contrib modules are protected by psql meta commands to
    # prevent running extension files in psql.
    # The SQL parser will error on those since they are not valid
    # SQL, so we comment out all psql meta commands before parsing.
    sql = re.sub(r"^\\", "-- \\\\", sql, flags=re.MULTILINE)

    if toplevel:
        state.counter.sql = sql

    visitor = SQLVisitor(state)
    for stmt in parse_sql(sql):
        if toplevel:
            state.counter.stmt_location = stmt.stmt_location
        visitor(stmt)


def visit_plpgsql(state, node, searchpath_secure=False):
    if not state.args.plpgsql:
        return

    match (node):
        case ast.CreateFunctionStmt():
            raw = raw_sql(node)

        case ast.DoStmt():
            raw = raw_sql(node)

        case _:
            state.unknown("Unknown node in visit_plpgsql: {}".format(node))
            return

    parsed = parse_plpgsql(raw)

    visitor = PLPGSQLVisitor(state)
    for item in parsed:
        visitor(item)


class PLPGSQLVisitor:
    def __init__(self, state):
        super(self.__class__, self).__init__()
        self.state = state

    def __call__(self, node):
        self.visit(node)

    def visit(self, node):
        if isinstance(node, list):
            for item in node:
                self.visit(item)
        if isinstance(node, dict):
            for key, value in node.items():
                match (key):
                    # work around inconsistent expression handling for assert and return statement in pglast
                    case "PLpgSQL_stmt_assert":
                        visit_sql(
                            self.state,
                            "SELECT " + value["cond"]["PLpgSQL_expr"]["query"],
                        )
                    case "PLpgSQL_stmt_return":
                        if value:
                            visit_sql(
                                self.state,
                                "SELECT " + value["expr"]["PLpgSQL_expr"]["query"],
                            )
                    case "PLpgSQL_expr":
                        visit_sql(self.state, value["query"])
                    case _:
                        self.visit(value)


class SQLVisitor(Visitor):
    def __init__(self, state):
        self.state = state
        super(self.__class__, self).__init__()

    def visit_A_Expr(self, ancestors, node):
        if len(node.name) != 2 and not self.state.searchpath_secure:
            self.state.warn(
                "PS001", "'{}' in {}".format(format_name(node.name), RawStream()(node))
            )

    def visit_CreateFunctionStmt(self, ancestors, node):
        # If the function creation is in a schema we created before we
        # consider it safe even with CREATE OR REPLACE since there would be
        # no way to precreate it.
        if (
            len(node.funcname) == 2
            and node.funcname[0].val in self.state.created_schemas
        ):
            pass
        # This function was created without OR REPLACE previously so
        # CREATE OR REPLACE is safe now.
        elif format_function(node) in self.state.created_functions:
            pass
        elif node.replace:
            self.state.error("PS002", "{}".format(format_function(node)))

        # keep track of functions created in this script in case they get replaced later
        if node.replace == False:
            self.state.created_functions.append(format_function(node))

        # check function body
        language = [l.arg.val for l in node.options if l.defname == "language"][0]
        # check for security definer explicitly
        security = [s.arg.val == 1 for s in node.options if s.defname == "security"]
        if len(security) > 0:
            security = security[0]
        else:
            security = False

        body = [b.arg[0].val for b in node.options if b.defname == "as"][0]
        setter = [
            s.arg
            for s in node.options
            if s.defname == "set" and s.arg.name == "search_path"
        ]

        if setter:
            body_secure = self.state.is_secure_searchpath(setter[0])
        else:
            body_secure = False

        # functions without explicit search_path will generate a warning unless they are SECURITY DEFINER
        if security and language != "c":
            if not setter:
                self.state.error("PS003", "{}".format(format_function(node)))
            elif not body_secure:
                self.state.error("PS004", "{}".format(format_function(node)))
        else:
            if language in ["sql", "plpgsql"]:
                if (
                    not body_secure
                    and format_function(node)
                    not in self.state.args.proc_without_search_path
                ):
                    self.state.warn("PS005", "{}".format(format_function(node)))

        match (language):
            case "sql":
                state = State(self.state.counter)
                state.searchpath_secure = body_secure

                visit_sql(state, body)
            case "plpgsql":
                state = State(self.state.counter)
                state.searchpath_secure = body_secure
                visit_plpgsql(state, node)
            case ("c" | "internal"):
                pass
            case _:
                self.state.unknown("Unknown function language: {}".format(language))

    def visit_CreateTransformStmt(self, ancestors, node):
        if node.replace:
            self.state.warn("PS006", "{}".format(format_name(node.type_name)))

    def visit_DefineStmt(self, ancestors, node):
        if len(node.defnames) == 1 and not self.state.searchpath_secure:
            self.state.warn("PS017", "{}".format(format_name(node.defnames)))

        match node.kind:
            # CREATE AGGREGATE
            case ObjectType.OBJECT_AGGREGATE:
                if node.replace:
                    if format_aggregate(node) not in self.state.created_aggregates:
                        if (
                            len(node.defnames) != 2
                            or node.defnames[0].val not in self.state.created_schemas
                        ):
                            self.state.error(
                                "PS007", "{}".format(format_aggregate(node))
                            )

                if not node.replace:
                    self.state.created_aggregates.append(format_aggregate(node))

            case _:
                if (hasattr(node, "replace") and node.replace) or (
                    hasattr(node, "if_not_exists") and node.if_not_exists
                ):
                    if (
                        len(node.defnames) != 2
                        or node.defnames[0].val not in self.state.created_schemas
                    ):
                        self.state.error(
                            "PS007", "{}".format(format_name(node.defnames))
                        )

    def visit_VariableSetStmt(self, ancestors, node):
        # only search_path relevant
        if node.name == "search_path":
            if node.kind == VariableSetKind.VAR_SET_VALUE:
                self.state.set_searchpath(node, node.is_local)
            if node.kind == VariableSetKind.VAR_RESET:
                self.state.reset_searchpath()

    def visit_CaseExpr(self, ancestors, node):
        if node.arg and not self.state.searchpath_secure:
            self.state.error("PS009", "{}".format(raw_sql(node)))

    def visit_CreateSchemaStmt(self, ancestors, node):
        if node.if_not_exists and node.schemaname not in self.state.created_schemas:
            self.state.error("PS010", "{}".format(node.schemaname))
        self.state.created_schemas.append(node.schemaname)

    def visit_CreateSeqStmt(self, ancestors, node):
        if (
            node.if_not_exists
            and node.sequence.schemaname not in self.state.created_schemas
        ):
            self.state.error("PS011", "{}".format(raw_sql(node.sequence)))

    def visit_CreateStmt(self, ancestors, node):
        # We consider table creation safe even with IF NOT EXISTS if it happens in a
        # schema created in this context
        if (
            "schemaname" in node.relation
            and node.relation.schemaname in self.state.created_schemas
        ):
            pass
        elif node.if_not_exists:
            self.state.error("PS012", "{}".format(format_name(node.relation)))

    def visit_CreateTableAsStmt(self, ancestors, node):
        if (
            node.if_not_exists
            and node.into.rel.schemaname not in self.state.created_schemas
        ):
            self.state.error("PS007", "{}".format(format_name(node.into.rel)))

    def visit_CreateForeignServerStmt(self, ancestors, node):
        if node.if_not_exists:
            self.state.error("PS013", "{}".format(node.servername))

    def visit_IndexStmt(self, ancestors, node):
        if (
            node.if_not_exists
            and node.relation.schemaname not in self.state.created_schemas
        ):
            self.state.error("PS014", "{}".format(format_name(node.idxname)))

    def visit_TypeCast(self, ancestors, node):
        if len(node.typeName.names) == 1 and not self.state.searchpath_secure:
            self.state.error(
                "PS017",
                "{} in {}".format(format_name(node.typeName.names), RawStream()(node)),
            )

    def visit_ViewStmt(self, ancestors, node):
        if (
            "schemaname" in node.view
            and node.view.schemaname in self.state.created_schemas
        ):
            pass
        elif node.replace:
            self.state.error("PS015", "{}".format(format_name(node.view)))

    def visit_DoStmt(self, ancestors, node):
        language = [l.arg.val for l in node.args if l.defname == "language"]

        if language:
            language = language[0]
        else:
            language = "plpgsql"

        match (language):
            case "plpgsql":
                visit_plpgsql(self.state, node, self.state.searchpath_secure)
            case _:
                self.state.unknown("Unknown language: {}".format(language))

    def visit_FuncCall(self, ancestors, node):
        if len(node.funcname) != 2 and not self.state.searchpath_secure:
            self.state.warn("PS016", "{}".format(format_name(node.funcname)))
        # Possibly evaluate argument to "sql-accepting" function
        function_name = format_name(node.funcname[-1])
        function_args = self.state.counter.args.sql_fn
        if function_name in function_args:
            for arg in node.args:
                # we can only evaluate constant expressions
                if isinstance(arg, ast.A_Const):
                    sql = arg.val.val
                    try:
                        # let's try and treat this as SQL. Might not work.
                        visit_sql(self.state, sql)
                    except ParseError:
                        pass

        # we want to treat pg_catalog.set_config('search_path',...) similar to SET search_path
        if (
            format_name(node.funcname) == "pg_catalog.set_config"
            and len(node.args) == 3
        ):
            if get_text(node.args[0]) == "search_path":
                schemas = [s.strip() for s in get_text(node.args[1]).split(",")]
                local = get_text(node.args[2]) in ["t", "true"]
                self.state.set_searchpath(schemas, local)

    def visit_RangeVar(self, ancestors, node):
        # a rangevar can reference CTEs which were previously defined
        cte_names = self.extract_cte_names(ancestors)
        if (
            not node.schemaname
            and node.relname not in cte_names
            and not self.state.searchpath_secure
        ):
            self.state.warn("PS017", "{}".format(node.relname))

    def extract_cte_names(self, ancestor):
        # Iterate through parents, obtaining the names of CTEs which were directly defined
        cte_names = set()
        while ancestor.parent.node is not None:
            node = ancestor.node
            if hasattr(node, "withClause") and node.withClause is not None:
                for cte in node.withClause.ctes:
                    cte_names.add(cte.ctename)
            ancestor = ancestor.parent
        return cte_names

    # SET LOCAL is only effective until end of transaction so we have to reset
    # searchpath_secure when we encounter transaction statement
    def visit_TransactionStmt(self, ancestors, node):
        # we ignore BEGIN here since you have to be in transaction to use SET LOCAL
        # so BEGIN would be noop
        if node.kind == TransactionStmtKind.TRANS_STMT_BEGIN:
            return

        if self.state.searchpath_local:
            self.state.searchpath_secure = False
            self.state.searchpath_local = False
