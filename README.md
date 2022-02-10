## pgspot

Spot vulnerabilities in extension update scripts.

### Usage

```
pgspot -h
usage: pgspot [-h] [-a] [FILE ...]

Spot vulnerabilities in PostgreSQL SQL scripts

positional arguments:
  FILE          file to check for vulnerabilities

options:
  -h, --help    show this help message and exit
  -a, --append  append files before checking
```

```
pgspot <<<"CREATE TABLE IF NOT EXISTS foo();"
Unsafe table creation: foo
Unqualified object reference: foo

Errors: 1 Warnings: 1 Unknown: 0
```

