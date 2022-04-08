DO
$body$
BEGIN
    --pgspot:allow(E001)
    --pgspot:allow(W002)
    CREATE FUNCTION foo() RETURNS VOID
    AS
        $fn$ $fn$
    LANGUAGE sql;

    CREATE FUNCTION bar() RETURNS VOID
    AS
        $fn$ $fn$
    LANGUAGE sql;

end;
$body$
;