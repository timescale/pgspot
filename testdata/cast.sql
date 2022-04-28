-- safe: int is automatically interpreted as pg_catalog.int
SELECT 1::int;

-- safe: int4 is the built-in pg_catalog.int4
SELECT 1::pg_catalog.int4;

-- unsafe: the cast is to a custom type, and the type is unqualified
SELECT 1::custom_type;

-- safe: the cast is to a schema-qualified custom type
SELECT 1::custom_schema.type;

-- unsafe: the destination type is not fully-qualified
SELECT '1'::int4;

-- unsafe: the destination type is not fully-qualified
SELECT int4 '1';

-- unsafe: the destination type is not fully-qualified
SELECT CAST('1' AS int4);
