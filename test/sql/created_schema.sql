CREATE SCHEMA test_schema;

CREATE COLLATION IF NOT EXISTS test_schema.collation3 (locale = 'fr_FR.utf8');
CREATE FOREIGN TABLE IF NOT EXISTS test_schema.unsafe_table4(c4444 text) SERVER server4;
CREATE MATERIALIZED VIEW IF NOT EXISTS test_schema.matview6 AS SELECT pg_catalog.now();
CREATE SEQUENCE IF NOT EXISTS test_schema.sequence8;
CREATE TABLE IF NOT EXISTS test_schema.table10(c10 text);
CREATE TABLE IF NOT EXISTS test_schema.table11 AS SELECT pg_catalog.now();
