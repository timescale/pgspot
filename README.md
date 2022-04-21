## pgspot

Spot vulnerabilities in PostgreSQL extension scripts.

pgspot checks extension scripts for following PostgreSQL security best
practices. In addition to checking extension scripts it can also be
used to check security definer functions or any other PostgreSQL SQL code.

pgspot checks for the following vulnerabilities:
- search_path-based attacks
- unsafe object creation

Consult the [reference](REFERENCE.md) for detailed documentation of the
vulnerabilities which pgspot detects, and their potential mitigations.

## Useful links
- [PostgreSQL security recommendations for extensions](https://www.postgresql.org/docs/current/extend-extensions.html#EXTEND-EXTENSIONS-SECURITY)

## Requirements

- python >= 3.10
- [pglast](https://github.com/lelit/pglast) ([recommended fork](https://github.com/svenklemm/pglast))
- [libpg_query](https://github.com/pganalyze/libpg_query) (indirectly through pglast)

Currently it is recommended to use the forked version of pglast as it pulls in some libpg_query changes ([9aad9fdb](https://github.com/pganalyze/libpg_query/commit/9aad9fdbd78a9cdb09cc8eb24adc703887c9e76d) and [a53865a4](https://github.com/pganalyze/libpg_query/commit/a53865a45fe1530fcd9ba3476986559a75de4d8d)) affecting pgspot functionality that are not part of the last release.

### Usage

```
> ./pgspot -h
usage: pgspot [-h] [-a] [--proc-without-search-path PROC] [--summary-only] [--plpgsql | --no-plpgsql] [--explain EXPLAIN] [--ignore IGNORE] [--sql-accepting SQL_FN] [FILE ...]

Spot vulnerabilities in PostgreSQL SQL scripts

positional arguments:
  FILE                  file to check for vulnerabilities

options:
  -h, --help            show this help message and exit
  -a, --append          append files before checking
  --proc-without-search-path PROC
                        whitelist functions without explicit search_path
  --summary-only        only print number of errors, warnings and unknowns
  --plpgsql, --no-plpgsql
                        Analyze PLpgSQL code (default: True)
  --explain EXPLAIN     Describe an error/warning code
  --ignore IGNORE       Ignore error or warning code
  --sql-accepting SQL_FN
                        Specify one or more sql-accepting functions
```

```
> ./pgspot --ignore PS017 <<<"CREATE TABLE IF NOT EXISTS foo();"
PS012: Unsafe table creation: foo

Errors: 1 Warnings: 0 Unknown: 0
```

#### SQL-accepting functions

It is a common pattern that SQL-accepting functions exist, which take a
string-like argument which will be executed as SQL. This can "hide" some SQL
from pgspot, as the string-like argument masks the SQL. With the
`--sql-accepting` argument, pgspot can be told about such functions.

Assuming a function named `execute_sql` which takes a SQL string as its first
argument, and executes it. With `pgspot --sql-accepting=execute_sql` we can
tell pgspot `execute_sql` may accept SQL. pgspot will attempt to unpack and
evaluate all arguments to that function as SQL.
