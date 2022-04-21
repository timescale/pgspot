from util import run


def test_create_old_style_aggregate():
    sql = """
    CREATE AGGREGATE aggregate(BASETYPE=complex,SFUNC=agg_sfunc,STYPE=internal);
    """
    output = run(sql)

    assert "PS017" in output


def test_create_new_style_aggregate():
    sql = """
    CREATE AGGREGATE sum (complex)
    (
        sfunc = complex_add,
        stype = complex,
        initcond = '(0,0)'
    );
    """
    output = run(sql)

    assert "PS017" in output
