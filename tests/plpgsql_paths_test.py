from pglast import parse_plpgsql
from pgspot.plpgsql import build_node
from pgspot.path import paths


def test_minimal_function():
    sql = """
    CREATE FUNCTION mini() RETURNS TEXT AS $$ BEGIN END $$;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    assert node.type == "PLpgSQL_function"

    pathes = list(paths(node))
    assert len(pathes) == 1

    path = pathes[0]
    assert path.root == node

    assert str(path) == "PLpgSQL_stmt_return()"


def test_do_block():
    sql = """
    DO $$ BEGIN END $$;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    assert node.type == "PLpgSQL_function"

    pathes = list(paths(node))
    assert len(pathes) == 1

    path = pathes[0]
    assert path.root == node

    assert str(path) == "PLpgSQL_stmt_return()"
