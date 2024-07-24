from util import run


sql = """
CREATE FUNCTION python_max(a integer, b integer) RETURNS integer AS $$
    return max(a, b)
$$ LANGUAGE plpython3u SET search_path TO 'pg_catalog', 'pg_temp'
;

CREATE FUNCTION tcl_max(integer, integer) RETURNS integer AS $$
    if {$1 > $2} {return $1}
    return $2
$$ LANGUAGE pltcl STRICT SET search_path TO 'pg_catalog', 'pg_temp'
;
"""


def test_unknown_lang_plpython3u():
    output = run(sql)
    assert "Unknown function language: plpython3u" in output


def test_unknown_lang_pltcl():
    output = run(sql)
    assert "Unknown function language: pltcl" in output


def test_ignore_lang_plpython3u():
    output = run(sql, list("--ignore-lang=plpython3u"))
    assert "Unknown function language: plpython3u" not in output


def test_ignore_lang_pltcl():
    output = run(sql, list("--ignore-lang=pltcl"))
    assert "Unknown function language: pltcl" not in output


def test_ignore_lang_plpython3u_pltcl():
    output = run(sql, ["--ignore-lang=plpython3u", "--ignore-lang=pltcl"])
    assert (
        "Unknown function language: pltcl" not in output
        and "Unknown function language: plpython3u" not in output
    )


def test_ignore_lang_upper():
    output = run(sql, ["--ignore-lang=PLPYTHON3U", "--ignore-lang=PLTCL"])
    assert (
        "Unknown function language: pltcl" not in output
        and "Unknown function language: plpython3u" not in output
    )
