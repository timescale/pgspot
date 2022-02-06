
from pglast.stream import RawStream, OutputStream
from pglast import ast

def raw_sql(node):
  return RawStream()(node)

def format_name(name):
  match(name):
    case str():
      return name
    case (list()|tuple()):
      return ".".join([format_name(p) for p in name])
    case ast.String():
      return name.val
    case ast.RangeVar():
      if name.schemaname:
        return "{}.{}".format(name.schemaname,name.relname)
      else:
        return name.relname
    case ast.TypeName():
      return ".".join([format_name(p) for p in name.names])
    case _:
      return name

def format_function(node):
  if node.parameters:
    args = ",".join([p.strip().strip("'") for p in raw_sql(node.parameters).split(";")])
  else:
    args = ""
  return "{}({})".format(format_name(node.funcname), args)

