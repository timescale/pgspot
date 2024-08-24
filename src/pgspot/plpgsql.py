#
# pglast returns PLpgSQL AST as a nested dict. This file contains some glue code
# to convert the nested dict into a tree of objects.
#
# Disable pylint warnings about class names cause we are trying to match the
# AST names used by PLpgSQL parser.
# pylint: disable-msg=C0103
# pylint: disable-msg=R0903


class PLpgSQLNode:
    def __init__(self, raw):
        self.type = list(raw.keys())[0]
        self.lineno = None
        for k, v in raw[self.type].items():
            setattr(self, k, build_node(v))

    def __str__(self):
        return f"{self.type}({self.lineno})"

    def __repr__(self):
        fields = self.__dict__.copy()
        fields.pop("type")
        return f"{self.type}({fields})"


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
