
-- unsafe call inside function
CREATE FUNCTION sqlfunc() RETURNS TEXT LANGUAGE SQL AS $$ SELECT unsafe_call3(); $$;

-- safe call inside function
CREATE FUNCTION sqlfunc() RETURNS TEXT LANGUAGE SQL AS $$ SELECT safe_call6(); $$ SET search_path TO 'pg_catalog';

-- unsafe call inside function, since search_path for body is not safe
SET search_path TO pg_catalog;
CREATE FUNCTION sqlfunc() RETURNS TEXT LANGUAGE SQL AS $$ SELECT unsafe_call10(); $$;

CREATE FUNCTION sqlfunc() RETURNS TEXT LANGUAGE SQL AS $$
SELECT unsafe_call13();
SET search_path TO pg_catalog;
SELECT safe_call15();
RESET search_path;
SELECT unsafe_call17();
SELECT foo.safe_call18();
$$;
