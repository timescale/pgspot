SELECT
    CASE a OPERATOR(pg_catalog.=) b
        WHEN true THEN 'true'
        WHEN false THEN 'false'
    END
    FROM my_schema.foo;
