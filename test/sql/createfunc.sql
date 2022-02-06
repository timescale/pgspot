
-- should warn about unsafe function and format
CREATE OR REPLACE FUNCTION unsafe3() RETURNS TEXT LANGUAGE SQL AS $$ SELECT unsafe_call3('%I','foo'); $$;
-- should warn about call
CREATE FUNCTION safe5() RETURNS TEXT LANGUAGE SQL AS $$ SELECT unsafe_call5('%I','foo'); $$;

-- safe
CREATE FUNCTION f8() RETURNS TEXT LANGUAGE SQL AS $$ SELECT unsafe_call8('%I','foo'); $$;

-- should not warn about since f2 was created in this script so replace is safe
CREATE OR REPLACE FUNCTION f8() RETURNS TEXT LANGUAGE SQL AS $$ SELECT pg_catalog.safe_call11('%I','foo'); $$;

-- not safe since signature is different
CREATE OR REPLACE FUNCTION f8(int) RETURNS TEXT LANGUAGE SQL AS $$ SELECT pg_catalog.safe_call14('%I','foo'); $$;

CREATE FUNCTION safe16() RETURNS TEXT LANGUAGE plpgsql AS $$
BEGIN
  RETURN unsafe_call18('%I','foo');
END; $$;
