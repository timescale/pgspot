from pglast import parse_plpgsql
from pgspot.plpgsql import build_node
from pgspot.path import paths


def test_loop():
    sql = """
    CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
    BEGIN
      LOOP
        EXECUTE cmd || '1';
        EXECUTE cmd || '2';
      END LOOP;
    END
    $$;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    pathes = list(paths(node))
    assert len(pathes) == 1

    assert (
        str(pathes[0])
        == "PLpgSQL_stmt_dynexecute(4) -> PLpgSQL_stmt_dynexecute(5) -> PLpgSQL_stmt_return()"
    )


def test_while_loop():
    sql = """
    CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
    BEGIN
      WHILE true LOOP
        EXECUTE cmd || '1';
        EXECUTE cmd || '2';
      END LOOP;
    END
    $$;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    pathes = list(paths(node))
    assert len(pathes) == 1

    assert (
        str(pathes[0])
        == "PLpgSQL_stmt_dynexecute(4) -> PLpgSQL_stmt_dynexecute(5) -> PLpgSQL_stmt_return()"
    )


def test_fori_loop():
    sql = """
    CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
    DECLARE
      i INT;
    BEGIN
      FOR i IN 1..10 LOOP
        RAISE NOTICE 'i is %',i;
      END LOOP;
    END
    $$;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    pathes = list(paths(node))
    assert len(pathes) == 1

    assert str(pathes[0]) == "PLpgSQL_stmt_raise(6) -> PLpgSQL_stmt_return()"


def test_fors_loop():
    sql = """
    CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
    DECLARE
      i INT;
    BEGIN
      FOR i IN SELECT generate_series(1,10) LOOP
        RAISE NOTICE 'i is %',i;
      END LOOP;
    END
    $$ LANGUAGE plpgsql;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    pathes = list(paths(node))
    assert len(pathes) == 1

    assert str(pathes[0]) == "PLpgSQL_stmt_raise(6) -> PLpgSQL_stmt_return()"


def test_dynfors_loop():
    sql = """
    CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
    DECLARE
      i INT;
    BEGIN
      FOR i IN EXECUTE 'SELECT generate_series(1,10)' LOOP
        RAISE NOTICE 'i is %',i;
      END LOOP;
    END
    $$ LANGUAGE plpgsql;
    """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    pathes = list(paths(node))
    assert len(pathes) == 1

    assert str(pathes[0]) == "PLpgSQL_stmt_raise(6) -> PLpgSQL_stmt_return()"


def test_forc_loop():
    sql = """
   CREATE FUNCTION foo(cmd TEXT) RETURNS void AS $$
   DECLARE
     i INT;
     c CURSOR FOR SELECT generate_series(1,10);
   BEGIN
     FOR i IN c LOOP
       RAISE NOTICE 'i is %',i;
     END LOOP;
   END
   $$ LANGUAGE plpgsql;
   """
    parsed = parse_plpgsql(sql)
    node = build_node(parsed[0])
    pathes = list(paths(node))
    assert len(pathes) == 1

    assert str(pathes[0]) == "PLpgSQL_stmt_raise(7) -> PLpgSQL_stmt_return()"
