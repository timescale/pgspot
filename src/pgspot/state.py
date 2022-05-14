from pglast import ast
from .codes import codes
from .formatters import get_text


class Counter:
    def __init__(self, args):
        self.args = args
        self.warnings = 0
        self.unknowns = 0
        self.errors = 0

        # for tracking current position in input stream
        # only toplevel visitor should update these
        self.sql = ""
        self.stmt_location = 0

    def add(self, counter):
        self.warnings += counter.warnings
        self.unknowns += counter.unknowns
        self.errors += counter.errors

    def print_issue(self, code, context):
        if code not in codes:
            raise ValueError
        if not self.args.summary_only:
            line = self.line_number()
            title = codes[code]["title"]
            print(
                "{code}: {title}: {context} at line {line}".format(
                    code=code, title=title, context=context, line=line
                )
            )

    def warn(self, code, context):
        if code not in self.args.ignore:
            self.warnings += 1
            self.print_issue(code, context)

    def error(self, code, context):
        if code not in self.args.ignore:
            self.errors += 1
            self.print_issue(code, context)

    # Unfortunately the line_number handling is not perfect.
    # This will be the line of the first character after the
    # previous statement has ended. On files with comments
    # before a statement it will indicate the line with comments
    # instead of the line with the actual statement.
    # Since these numbers are reported to us by pglast/libpg_query
    # there is not much more here we can do to improve accuracy.
    def line_number(self):
        return 1 + self.sql.count("\n", 0, self.stmt_location + 1)

    def unknown(self, message):
        self.unknowns += 1
        if not self.args.summary_only:
            print(message)

    def is_clean(self):
        return self.errors + self.warnings + self.unknowns == 0

    def __str__(self):
        return "Errors: {} Warnings: {} Unknown: {}".format(
            self.errors, self.warnings, self.unknowns
        )


class State:
    def __init__(self, counter):
        self.counter = counter
        self.args = counter.args
        self.created_schemas = list()
        self.created_aggregates = list()
        self.created_functions = list()
        self.searchpath_secure = False
        self.searchpath_local = False

    def warn(self, code, context):
        self.counter.warn(code, context)

    def error(self, code, context):
        self.counter.error(code, context)

    def unknown(self, message):
        self.counter.unknown(message)

    def set_searchpath(self, stmt, local=False):
        self.searchpath_secure = self.is_secure_searchpath(stmt)
        self.searchpath_local = local

    def reset_searchpath(self):
        self.searchpath_secure = False
        self.searchpath_local = False

    def extract_schemas(self, setters):
        match (setters):
            case str():
                return [setters]
            case list():
                return setters
            case ast.VariableSetStmt():
                return [get_text(item) for item in setters.args]
            case _:
                raise Exception("Unhandled type in extract_schemas: {}".format(setters))

    # we consider the search path safe when it only contains
    # pg_catalog and any schema created in this script and
    # pg_temp as last entry
    def is_secure_searchpath(self, setters):
        schemas = self.extract_schemas(setters)

        # explicit pg_catalog at start of search_path is fine
        if schemas[0] == "pg_catalog":
            schemas = schemas[1:]

        # any schema created by us is fine too
        while len(schemas) and schemas[0] in self.created_schemas:
            schemas = schemas[1:]

        # we require explicit pg_temp as last entry for a schema to
        # be safe because not having explicit pg_temp in search_path
        # will result in a search_path with pg_temp as first entry
        if schemas == ["pg_temp"]:
            return True

        return False
