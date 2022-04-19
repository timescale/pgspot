
from pglast import ast
from codes import codes

class Counter():
  def __init__(self, args):
    self.args = args
    self.warnings = 0
    self.unknowns = 0
    self.errors = 0

    self.created_schemas = list()
    self.created_functions = list()

  def warn(self, code, context):
    if code not in self.args.ignore:
      self.warnings += 1
      if code not in codes:
        raise ValueError
      if not self.args.summary_only:
        print("{}: {}: {}".format(code, codes[code]['title'], context))

  def error(self, code, context):
    if code not in self.args.ignore:
      self.errors += 1
      if code not in codes:
        raise ValueError
      if not self.args.summary_only:
        print("{}: {}: {}".format(code, codes[code]['title'], context))

  def unknown(self, message):
    self.unknowns += 1
    if not self.args.summary_only:
      print(message)

  def is_clean(self):
    return self.errors + self.warnings + self.unknowns == 0

  def __str__(self):
    return "\nErrors: {} Warnings: {} Unknown: {}".format(self.errors, self.warnings, self.unknowns)

class State():
  def __init__(self, counter):
    self.counter = counter
    self.args = counter.args
    self.created_schemas = list()
    self.created_functions = list()
    self.searchpath_secure = False
    self.searchpath_local = False

  def warn(self, code, context):
    self.counter.warn(code, context)

  def error(self, code, context):
    self.counter.error(code, context)

  def unknown(self, message):
    self.counter.unknown(message)

  def set_searchpath(self, stmt):
    self.searchpath_secure = self.is_secure_searchpath(stmt)
    self.searchpath_local = stmt.is_local

  def reset_searchpath(self):
    self.searchpath_secure = False
    self.searchpath_local = False

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

