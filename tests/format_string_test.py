
from pgspot.pg_catalog.format import parse_format_string


def test_no_variables():
    ret = parse_format_string("")
    assert ret == []

    ret = parse_format_string("SELECT * FROM table")
    assert ret == []

    ret = parse_format_string("%%")
    assert ret == []

