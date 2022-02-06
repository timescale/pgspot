
from pglast import ast

class GlobalState():
  def __init__(self):
    self.warnings = 0
    self.unknowns = 0

    self.builtin_types = ['bool','bytea','int','jsonb','name','regclass','text','record']
    self.created_schemas = list()
    self.created_functions = list()

  def warn(self, message):
    self.warnings += 1
    print(message)

  def unknown(self, message):
    self.unknown += 1
    print(message)

  # we consider the search path safe when it only contains
  # pg_catalog and any schema created in this script
  def is_secure_searchpath(self, setters):
    secure = False

    match(setters):
      case str():
        secure = setters == 'pg_catalog' or setters in self.created_schemas
      case (list()|tuple()):
        secure = all([self.is_secure_searchpath(item) for item in setters])
      case (ast.A_Const()|ast.String()):
        secure = self.is_secure_searchpath(setters.val)
      case ast.VariableSetStmt():
        secure = self.is_secure_searchpath(setters.args)
      case _:
        raise Exception("Unhandled type in is_secure_searchpath: {}".format(setters))

    return secure

  def __str__(self):
    return "Warnings: {} Unknown: {}".format(self.warnings, self.unknowns)

