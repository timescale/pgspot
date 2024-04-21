-- unsafe sec definer with no search_path
CREATE FUNCTION unsafe_sec_definer2() RETURNS TEXT LANGUAGE SQL SECURITY DEFINER AS $$ SELECT now(); $$;
-- same function but with security invoker should only give warning
CREATE FUNCTION safe_sec_invoker4() RETURNS TEXT LANGUAGE SQL SECURITY INVOKER AS $$ SELECT pg_catalog.now(); $$;
-- unsafe plpgsql sec definer with no search_path
CREATE FUNCTION unsafe_sec_definer6() RETURNS TEXT LANGUAGE PLPGSQL SECURITY DEFINER AS $$ BEGIN RETURN pg_catalog.now(); END; $$;
-- same function but with security invoker should only give warning
CREATE FUNCTION safe_sec_definer8() RETURNS TEXT LANGUAGE PLPGSQL SECURITY INVOKER AS $$ BEGIN RETURN pg_catalog.now(); END; $$;
-- unsafe plpgsql sec definer procedure with no search_path
CREATE PROCEDURE unsafe_sec_definer10() LANGUAGE PLPGSQL SECURITY DEFINER AS $$ BEGIN PERFORM pg_catalog.now(); END; $$;
-- security definer function in C without search_path
CREATE FUNCTION c_sec_definer12() RETURNS TEXT LANGUAGE C SECURITY DEFINER AS 'c_sec_definer12';
