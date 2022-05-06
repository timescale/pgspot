from util import run


def test_global_ignore():
    sql = """
    CREATE TABLE IF NOT EXISTS foo();
    """
    output = run(sql)

    assert "PS012" in output
    assert "PS017" in output

    sql = """
    CREATE TABLE IF NOT EXISTS foo();
    """
    args = ["--ignore PS012"]
    output = run(sql, args)

    assert "PS012" not in output
    assert "PS017" in output
