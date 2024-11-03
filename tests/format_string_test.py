from pgspot.pg_catalog.format import parse_format_string

# %[position][flags][width]type


def test_no_variables():
    assert parse_format_string("") == []
    assert parse_format_string("SELECT * FROM table") == []
    assert parse_format_string("%%") == []


def test_single_variable():
    assert parse_format_string("%s") == [("s", 1)]
    assert parse_format_string("%I") == [("I", 1)]
    assert parse_format_string("%L") == [("L", 1)]

    assert parse_format_string("%%%s%%") == [("s", 1)]

    assert parse_format_string("%1$s") == [("s", 1)]
    assert parse_format_string("%3$s") == [("s", 3)]

    assert parse_format_string("%-s") == [("s", 1)]
    assert parse_format_string("%-10s") == [("s", 1)]
    assert parse_format_string("%-*s") == [("s", 2)]
    assert parse_format_string("%-*1$s") == [("s", 1)]

    assert parse_format_string("%7$-s") == [("s", 7)]
    assert parse_format_string("%7$-10s") == [("s", 7)]
    assert parse_format_string("%7$-*s") == [("s", 7)]
    assert parse_format_string("%7$-*1$s") == [("s", 7)]


def test_multiple_variable():
    assert parse_format_string("%s%I%L") == [("s", 1), ("I", 2), ("L", 3)]
    assert parse_format_string("%3$s%2$I%1$L") == [("s", 3), ("I", 2), ("L", 1)]
