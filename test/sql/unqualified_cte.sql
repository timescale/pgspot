WITH cte1 AS (
    VALUES (1)
), cte2 AS (
    WITH foo AS (
        SELECT * FROM cte1
    )
    SELECT * FROM foo
), cte3 AS (
    SELECT * FROM foo -- This will warn, foo is not a previously defined CTE
)
SELECT * FROM cte1 AS c1
    CROSS JOIN cte2
    CROSS JOIN cte3;
