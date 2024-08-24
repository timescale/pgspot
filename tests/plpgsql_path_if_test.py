from pglast import parse_plpgsql
from pgspot.plpgsql import build_node
from pgspot.path import paths


def test_if_minimal_stmt():
    sql = """
    CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
    BEGIN
      IF EXISTS (SELECT FROM pg_stat_activity) THEN
        EXECUTE cmd || '1';
      END IF;
    END
    $$;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    assert node.type == "PLpgSQL_function"

    pathes = list(paths(node))
    assert len(pathes) == 1

    assert (
        str(pathes[0])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(4) -> PLpgSQL_stmt_return()"
    )


def test_if_else():
    sql = """
    CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
    BEGIN
      IF EXISTS (SELECT FROM pg_stat_activity) THEN
        EXECUTE cmd || '1';
      ELSIF EXISTS (SELECT FROM pg_stat_activity) THEN
        EXECUTE cmd || '2';
      ELSIF EXISTS (SELECT FROM pg_stat_activity) THEN
        EXECUTE cmd || '3';
      ELSIF EXISTS (SELECT FROM pg_stat_activity) THEN
        EXECUTE cmd || '4';
      ELSE
        EXECUTE cmd || '5';
      END IF;
    END
    $$;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    assert node.type == "PLpgSQL_function"

    pathes = list(paths(node))
    assert len(pathes) == 5

    assert (
        str(pathes[0])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(4) -> PLpgSQL_stmt_return()"
    )
    assert (
        str(pathes[1])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(6) -> PLpgSQL_stmt_return()"
    )
    assert (
        str(pathes[2])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(8) -> PLpgSQL_stmt_return()"
    )
    assert (
        str(pathes[3])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(10) -> PLpgSQL_stmt_return()"
    )
    assert (
        str(pathes[4])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(12) -> PLpgSQL_stmt_return()"
    )


def test_if_stmt():
    sql = """
    CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
    BEGIN
      IF EXISTS (SELECT 1 FROM pg_stat_activity) THEN
          EXECUTE cmd || '1';
      ELSE
          EXECUTE cmd || '2';
          RETURN 'foo';
      END IF;
      IF EXISTS (SELECT 1 FROM pg_stat_activity) THEN
        EXECUTE cmd;
      ELSE
        EXECUTE cmd;
      END IF;
    END
    $$;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    assert node.type == "PLpgSQL_function"

    pathes = list(paths(node))
    assert len(pathes) == 3

    assert (
        str(pathes[0])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(4) -> PLpgSQL_stmt_if(9) -> PLpgSQL_stmt_dynexecute(10) -> PLpgSQL_stmt_return()"
    )
    assert (
        str(pathes[1])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(6) -> PLpgSQL_stmt_return(7)"
    )
    assert (
        str(pathes[2])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(4) -> PLpgSQL_stmt_if(9) -> PLpgSQL_stmt_dynexecute(12) -> PLpgSQL_stmt_return()"
    )


def test_nested_if_stmt():
    sql = """
    CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
    BEGIN
      IF EXISTS (SELECT FROM pg_stat_activity) THEN
        EXECUTE cmd || '1';
      ELSE
        IF EXISTS (SELECT FROM pg_stat_activity) THEN
          EXECUTE cmd || '2';
        ELSE
          EXECUTE cmd || '3';
        END IF;
      END IF;
    END
    $$;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    assert node.type == "PLpgSQL_function"

    pathes = list(paths(node))
    assert len(pathes) == 3

    assert (
        str(pathes[0])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_dynexecute(4) -> PLpgSQL_stmt_return()"
    )
    assert (
        str(pathes[1])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_if(6) -> PLpgSQL_stmt_dynexecute(7) -> PLpgSQL_stmt_return()"
    )
    assert (
        str(pathes[2])
        == "PLpgSQL_stmt_if(3) -> PLpgSQL_stmt_if(6) -> PLpgSQL_stmt_dynexecute(9) -> PLpgSQL_stmt_return()"
    )
