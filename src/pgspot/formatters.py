from pglast.stream import RawStream, OutputStream
from pglast import ast


def raw_sql(node):
    return RawStream()(node)


def get_text(node):
    match (node):
        case str():
            return node
        case ast.A_Const():
            return get_text(node.val)
        case ast.String():
            return node.val
        case _:
            return str(node)


def format_name(name):
    match (name):
        case str():
            return name
        case (list() | tuple()):
            return ".".join([format_name(p) for p in name])
        case ast.String():
            return name.val
        case ast.RangeVar():
            if name.schemaname:
                return "{}.{}".format(name.schemaname, name.relname)
            else:
                return name.relname
        case ast.TypeName():
            return ".".join([format_name(p) for p in name.names])
        case _:
            return str(name)


def format_function(node):
    if node.parameters:
        args = ",".join(
            [p.strip().strip("'") for p in raw_sql(node.parameters).split(";")]
        )
    else:
        args = ""
    return "{}({})".format(format_name(node.funcname), args)


def format_aggregate(node):
    if node.oldstyle:
        basetype = [b.arg.names for b in node.definition if b.defname == "basetype"]
        if basetype:
            basetype = basetype[0]

        if not basetype:
            args = ""
        elif len(basetype) == 2 and basetype[0].val == "pg_catalog":
            args = basetype[1].val
        else:
            args = ",".join([s.val for s in basetype])
    else:
        args = ",".join([raw_sql(arg.argType) for arg in node.args[0]])
    return "{}({})".format(format_name(node.defnames), args)
