
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

-- safe creation
CREATE FUNCTION f22(a int = 1) RETURNS TEXT LANGUAGE SQL AS $$ SELECT 'foo'; $$ SET search_path TO pg_catalog,pg_temp;

-- safe as well since it was previously created with same signature but different default
CREATE OR REPLACE FUNCTION f22(a int = 2) RETURNS TEXT LANGUAGE SQL AS $$ SELECT 'foo'; $$ SET search_path TO pg_catalog,pg_temp;

-- not safe since it's new signature
CREATE OR REPLACE FUNCTION f22(b int) RETURNS TEXT LANGUAGE SQL AS $$ SELECT 'foo'; $$ SET search_path TO pg_catalog,pg_temp;
