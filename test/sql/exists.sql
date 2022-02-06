-- test if not exists

CREATE COLLATION IF NOT EXISTS collation3 (locale = 'fr_FR.utf8');
CREATE FOREIGN TABLE IF NOT EXISTS unsafe_table4(c4444 text) SERVER server4;
CREATE INDEX IF NOT EXISTS index5 ON table5(column5);
CREATE MATERIALIZED VIEW IF NOT EXISTS matview6 AS SELECT pg_catalog.now();
CREATE SCHEMA IF NOT EXISTS schema7;
CREATE SEQUENCE IF NOT EXISTS sequence8;
CREATE SERVER IF NOT EXISTS server9 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'foo', dbname 'foodb', port '5432');
CREATE TABLE IF NOT EXISTS table10(c10 text);
CREATE TABLE IF NOT EXISTS table11 AS SELECT pg_catalog.now();

