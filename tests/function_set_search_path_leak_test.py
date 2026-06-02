from util import run


# A function's `SET search_path` only applies while that function executes; it
# must not mark the rest of the script as having a secure search_path.
def test_function_set_search_path_does_not_leak_to_later_statement():
    sql = """
    CREATE FUNCTION f() RETURNS int LANGUAGE sql
        SET search_path = pg_catalog, pg_temp
    AS $$ SELECT 1 $$;
    SELECT unsafe_call();
    """
    output = run(sql)

    assert "PS016" in output


# An anonymous DO block runs under the session search_path, not under any
# preceding function's `SET search_path`, so unqualified references inside it
# must still be flagged.
def test_function_set_search_path_does_not_leak_into_do_block():
    sql = """
    CREATE FUNCTION f() RETURNS int LANGUAGE sql
        SET search_path = pg_catalog, pg_temp
    AS $$ SELECT 1 $$;
    DO $$ BEGIN PERFORM unsafe_do_call(); END $$;
    """
    output = run(sql)

    assert "PS016" in output


# `ALTER FUNCTION ... SET search_path` likewise only affects that function, so
# it must not mark later statements as secure either.
def test_alter_function_set_search_path_does_not_leak_to_later_statement():
    sql = """
    CREATE FUNCTION f() RETURNS int LANGUAGE sql AS $$ SELECT 1 $$;
    ALTER FUNCTION f() SET search_path = pg_catalog, pg_temp;
    SELECT unsafe_after_alter();
    """
    output = run(sql)

    assert "PS016" in output


# `ALTER FUNCTION ... RESET search_path` only affects that function, so it must
# not reset the file-level secure state established by a real top-level SET.
def test_function_reset_search_path_does_not_leak_to_later_statement():
    sql = """
    SET search_path = pg_catalog, pg_temp;
    CREATE FUNCTION f() RETURNS int LANGUAGE sql AS $$ SELECT 1 $$;
    ALTER FUNCTION f() RESET search_path;
    SELECT now();
    """
    output = run(sql)

    assert "PS016" not in output
