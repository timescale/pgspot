import subprocess
import shlex


def test_create_old_style_aggregate():
    sql = """
    CREATE AGGREGATE aggregate(SFUNC=agg_sfunc,STYPE=internal);
    """
    result = subprocess.run(
        ["echo {} | python pgspot".format(shlex.quote(sql))],
        shell=True,
        capture_output=True,
        text=True,
    )
    output = result.stdout

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
    result = subprocess.run(
        ["echo {} | python pgspot".format(shlex.quote(sql))],
        shell=True,
        capture_output=True,
        text=True,
    )
    output = result.stdout

    assert "PS017" in output
