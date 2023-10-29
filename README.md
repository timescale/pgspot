## pgspot
<p align="center">
  <a href="https://github.com/timescale/pgspot/actions"><img alt="Actions Status" src="https://github.com/timescale/pgspot/workflows/Test/badge.svg"></a>
  <a href="https://github.com/timescale/pgspot/blob/main/LICENSE"><img alt="License: PostgreSQL" src="https://img.shields.io/github/license/timescale/pgspot"></a>
  <a href="https://pypi.org/project/pgspot/"><img alt="PyPI" src="https://img.shields.io/pypi/v/pgspot"></a>
  <a href="https://pepy.tech/project/pgspot"><img alt="Downloads" src="https://pepy.tech/badge/pgspot"></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <a href="https://www.bestpractices.dev/projects/8009"><img src="https://www.bestpractices.dev/projects/8009/badge"></a>
</p>

Spot vulnerabilities in PostgreSQL extension scripts.

pgspot checks extension scripts for following PostgreSQL security best
practices. In addition to checking extension scripts it can also be
used to check security definer functions or any other PostgreSQL SQL code.

pgspot checks for the following vulnerabilities:
- search_path-based attacks
- unsafe object creation

Consult the [reference] for detailed documentation of the vulnerabilities which
pgspot detects, and their potential mitigations.

[reference]: https://github.com/timescale/pgspot/blob/main/REFERENCE.md

## Useful links
- [PostgreSQL security recommendations for extensions](https://www.postgresql.org/docs/current/extend-extensions.html#EXTEND-EXTENSIONS-SECURITY)
- [PostgreSQL security recommendations for SECURITY DEFINER functions](https://www.postgresql.org/docs/current/sql-createfunction.html#SQL-CREATEFUNCTION-SECURITY)

## Installation

pip install pgspot

## Requirements

- python >= 3.10
- [pglast == 5.0](https://github.com/lelit/pglast)
- [libpg_query](https://github.com/pganalyze/libpg_query) (through pglast)

To install the runtime requirements, use `pip -r requirements.txt`.


### Usage

```
> pgspot -h
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
> pgspot --ignore PS017 <<<"CREATE TABLE IF NOT EXISTS foo();"
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
