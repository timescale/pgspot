from pgspot import state
import pglast


def test_search_path():
    s = state.State(state.Counter({}))

    assert s.is_secure_searchpath("pg_temp")
    assert s.is_secure_searchpath(["pg_temp"])
    assert s.is_secure_searchpath(["pg_catalog", "pg_temp"])
    assert not s.is_secure_searchpath("pg_catalog")
    assert not s.is_secure_searchpath(["pg_catalog"])
    assert not s.is_secure_searchpath(["pg_temp", "pg_catalog"])

    stmts = pglast.parse_sql("SET search_path TO pg_catalog;")
    assert not s.is_secure_searchpath(stmts[0].stmt)

    stmts = pglast.parse_sql("SET search_path TO pg_catalog, pg_temp;")
    assert s.is_secure_searchpath(stmts[0].stmt)

    stmts = pglast.parse_sql("SET search_path TO pg_temp, pg_catalog;")
    assert not s.is_secure_searchpath(stmts[0].stmt)
