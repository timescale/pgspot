
## 0.5.0 (2023-02-24)

- Update pglast to 5.0 which makes pgspot use the PostgreSQL 15 parser #84

## 0.4.0 (2023-01-03)

- Update pglast to 4.1 which makes pgspot use the PostgreSQL 14 parser #79

## 0.3.3 (2022-08-14)

- Adjust documentation to mention PG upstream changes regarding CREATE OR REPLACE and CREATE IF NOT EXISTS
- Update pglast to >= 3.13 #74

## 0.3.2 (2022-06-20)

- Add support for pg_catalog.set_config() for search_path tracking #66
- Fix RangeFunction handling #69
- Update pglast to >= 3.11 #71

## 0.3.1 (2022-05-12)

## 0.3.0 (2022-05-12)

- Fix counter reporting for append mode #56
- Update pglast to >= 3.10 #58

## 0.2.0 (2022-05-02)

- Print line numbers in warnings and errors #44
- Don't raise exception on unknown DO block language #49
- Add per file counter tracking in multiple file mode #50
- Don't warn about search_path of C SECURITY DEFINER functions #52
- Fix search_path evaluation #53

## 0.1.1 (2022-04-22)

- Add aggregate creation tracking #42

## 0.1.0 (2022-04-21)

- Initial release

