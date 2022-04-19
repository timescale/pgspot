from util import run


def test_call_sql_accepting_function():
    sql = """
    CALL some_schema.execute_sql($ee$
      DO $DO$
      BEGIN
        SELECT unsafe_call();
      END $DO$;
    $ee$);
    """
    args = ["--sql-accepting=execute_sql"]
    output = run(sql, args)

    assert "PS016" in output


def test_select_sql_accepting_function():
    sql = """
    SELECT some_schema.execute_sql($ee$
      DO $DO$
      BEGIN
        SELECT unsafe_call();
      END $DO$;
    $ee$);
    """
    args = ["--sql-accepting=execute_sql"]
    output = run(sql, args)

    assert "PS016" in output


def test_select_sql_accepting_function_with_non_sql():
    sql = """
    SELECT some_schema.execute_sql(some_parameter);
    """
    args = ["--sql-accepting=execute_sql"]
    output = run(sql, args)

    assert "Errors: 0 Warnings: 0" in output
