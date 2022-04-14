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
- pglast

### Usage

```
> ./pgspot -h
usage: pgspot [-h] [-a] [--proc-without-search-path PROC] [--summary-only] [--plpgsql | --no-plpgsql] [--explain EXPLAIN] [FILE ...]

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
```

```
> ./pgspot <<<"CREATE TABLE IF NOT EXISTS foo();"
E009: Unsafe table creation: foo
W005: Unqualified object reference: foo

Errors: 1 Warnings: 1 Unknown: 0
```

