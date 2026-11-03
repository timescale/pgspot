from util import run


# The relations named in FOR UPDATE/SHARE OF refer to entries in the FROM
# clause (usually aliases) and Postgres does not allow them to be schema
# qualified, so they are not object references and must not trigger PS017.
def test_locking_clause_alias_is_not_unqualified_reference():
    sql = """
    SELECT t.id FROM public.task AS t FOR UPDATE OF t SKIP LOCKED;
    """
    output = run(sql)

    assert "PS017" not in output


def test_locking_clause_alias_in_cte():
    sql = """
    WITH s AS (
        SELECT t.id FROM public.task AS t
        LEFT JOIN pg_catalog.pg_locks AS l ON l.pid OPERATOR(pg_catalog.=) t.pid
        WHERE l.pid IS NULL
        FOR NO KEY UPDATE OF t, l
    ) SELECT s.id FROM s;
    """
    output = run(sql)

    assert "PS017" not in output


def test_unqualified_relation_with_locking_clause_still_warns():
    sql = """
    SELECT task.id FROM task FOR UPDATE OF task;
    """
    output = run(sql)

    assert "PS017: Unqualified object reference: task" in output
    assert output.count("PS017") == 1
