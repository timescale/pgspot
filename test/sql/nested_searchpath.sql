
SELECT unsafe_call2();

SET search_path TO pg_catalog;

SELECT safe_call6();

-- safe because search_path is locked down
DO $$ BEGIN SELECT safe_call_in_do9(); END; $$;
CREATE FUNCTION f10_no_path() RETURNS TEXT LANGUAGE SQL AS $$ SELECT unsafe_call10(); $$;

RESET search_path;

-- unsafe because search_path is not locked down
DO $$ BEGIN SELECT unsafe_call_in_do14(); END; $$;

SET search_path TO pg_catalog;

CREATE FUNCTION f18_no_path() RETURNS TEXT LANGUAGE SQL AS $$ SELECT unsafe_call18(); $$;
CREATE FUNCTION f19_path() RETURNS TEXT LANGUAGE SQL SET search_path TO public AS $$ SELECT unsafe_call19(); $$;

CREATE FUNCTION f21_path() RETURNS TEXT LANGUAGE SQL SET search_path TO pg_catalog AS $$ SELECT safe_call21(); $$;

CREATE FUNCTION f23_path() RETURNS TEXT LANGUAGE SQL SET search_path TO pg_catalog AS $$
  -- search_path is not inherited in inner function body
  CREATE FUNCTION f25_nested_no_path() RETURNS TEXT LANGUAGE SQL AS $f1$ SELECT unsafe_call25(); $f1$;
$$;
