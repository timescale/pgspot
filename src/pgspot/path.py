# pylint: disable=fixme


class Path:
    """A path is a sequence of steps that will be executed in a PLpgSQL function."""

    def __init__(self, root, steps=None, stack=None):
        self.root = root
        # steps is the list of nodes that have been processed
        self.steps = steps.copy() if steps else []
        # stack is a list of nodes that are yet to be processed
        self.stack = stack.copy() if stack else []

    def copy(self):
        return Path(self.root, self.steps, self.stack)

    def __str__(self):
        return " -> ".join([str(step) for step in self.steps])


def paths(root):
    p = Path(root)
    pathes = []
    dfs(root, p, pathes)
    yield p

    while pathes:
        p = pathes.pop(0)
        t = p.stack.pop(0)
        dfs(t, p, pathes)
        yield p


def dfs(node, path, pathes):
    """traverse tree depth first similar to how it would get executed"""
    if not node:
        return
    if node:
        match node.type:
            case "PLpgSQL_function":
                # This should be top level node and so stack should be empty
                assert not path.stack
                path.stack = [node.action] + path.stack
            case "PLpgSQL_stmt_block":
                # FIXME: Add support for exception handling
                path.stack = node.body + path.stack
            case "PLpgSQL_stmt_if":
                path.steps.append(node)
                if node.elsif_list:
                    for elsif in node.elsif_list:
                        alt = path.copy()
                        alt.stack = elsif.stmts + alt.stack
                        pathes.append(alt)
                if node.else_body:
                    alt = path.copy()
                    alt.stack = node.else_body + alt.stack
                    pathes.append(alt)

                path.stack = node.then_body + path.stack

            # different types of loops
            # FIXME: Add support for loop exit
            case (
                "PLpgSQL_stmt_loop"
                | "PLpgSQL_stmt_while"
                | "PLpgSQL_stmt_forc"
                | "PLpgSQL_stmt_fori"
                | "PLpgSQL_stmt_fors"
                | "PLpgSQL_stmt_dynfors"
            ):
                path.stack = node.body + path.stack

            # nodes with no children
            case (
                "PLpgSQL_stmt_assert"
                | "PLpgSQL_stmt_assign"
                | "PLpgSQL_stmt_call"
                | "PLpgSQL_stmt_close"
                | "PLpgSQL_stmt_commit"
                | "PLpgSQL_stmt_dynexecute"
                | "PLpgSQL_stmt_execsql"
                | "PLpgSQL_stmt_fetch"
                | "PLpgSQL_stmt_getdiag"
                | "PLpgSQL_stmt_open"
                | "PLpgSQL_stmt_perform"
                | "PLpgSQL_stmt_raise"
                | "PLpgSQL_stmt_return_next"
                | "PLpgSQL_stmt_return_query"
                | "PLpgSQL_stmt_rollback"
            ):
                path.steps.append(node)

            # nodes not yet implemented
            case "PLpgSQL_stmt_case" | "PLpgSQL_stmt_exit" | "PLpgSQL_stmt_foreach_a":
                raise Exception(f"Not yet implemented {node.type}")

            # nodes that will end current path
            case "PLpgSQL_stmt_return":
                path.steps.append(node)
                path.stack.clear()
                return

            case _:
                raise Exception(f"Unknown node type {node.type}")

    while path.stack:
        t = path.stack.pop(0)
        dfs(t, path, pathes)
