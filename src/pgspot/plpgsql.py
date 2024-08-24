#
# pglast returns PLpgSQL AST as a nested dict. This file contains some glue code
# to convert the nested dict into a tree of objects.
#
# Disable pylint warnings about class names cause we are trying to match the
# AST names used by PLpgSQL parser.
# pylint: disable-msg=invalid-name,too-few-public-methods


class PLpgSQLNode:
    def __init__(self, raw):
        self.type = list(raw.keys())[0]
        self.lineno = ""
        for k, v in raw[self.type].items():
            setattr(self, k, build_node(v))

    def __str__(self):
        return f"{self.type}({self.lineno})"

    def __repr__(self):
        fields = self.__dict__.copy()
        fields.pop("type")
        return f"{self.type}({fields})"


class PLpgSQL_stmt_if(PLpgSQLNode):
    def __init__(self, raw):
        self.then_body = None
        self.elsif_list = None
        self.else_body = None
        super().__init__(raw)


class PLpgSQL_row(PLpgSQLNode):
    def __init__(self, raw):
        # PLpgSQL_row has a fields attribute which is a list of dicts that
        # don't have the same structure as other node dicts. So we pop it out
        # and set it as an attribute directly instead of having it handled by
        # recursion.
        self.fields = raw["PLpgSQL_row"].pop("fields")
        super().__init__(raw)


class PLpgSQL_var(PLpgSQLNode):
    def __init__(self, raw):
        self.refname = None
        self.datatype = None
        super().__init__(raw)

    def __str__(self):
        return f"Variable(name={self.refname} type={self.datatype})"


def build_node(node):
    if isinstance(node, list):
        return [build_node(n) for n in node]
    if isinstance(node, dict):
        name = list(node.keys())[0]
        if globals().get(name) is not None:
            return globals()[name](node)
        return PLpgSQLNode(node)

    return node
