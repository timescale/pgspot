
-- unsafe call inside function
CREATE FUNCTION plpgsqlfunc3() RETURNS TEXT LANGUAGE PLPGSQL AS $$ BEGIN SELECT unsafe_call3(); END; $$;
CREATE FUNCTION plpgsqlfunc4() RETURNS TEXT LANGUAGE PLPGSQL AS $$ BEGIN PERFORM unsafe_call4(); END; $$;
CREATE FUNCTION plpgsqlfunc5() RETURNS TEXT LANGUAGE PLPGSQL AS $$ BEGIN RETURN unsafe_call5(); END; $$;

-- safe call inside function
CREATE FUNCTION plpgsqlfunc7() RETURNS TEXT LANGUAGE PLPGSQL AS $$ BEGIN SELECT safe_call7(); END; $$ SET search_path TO 'pg_catalog';
CREATE FUNCTION plpgsqlfunc8() RETURNS TEXT LANGUAGE PLPGSQL AS $$ BEGIN PERFORM safe_call8(); END; $$ SET search_path TO 'pg_catalog';

-- unsafe call inside function, since search_path for body is not safe
SET search_path TO pg_catalog;
CREATE FUNCTION plpgsqlfunc13() RETURNS TEXT LANGUAGE PLPGSQL AS $$ BEGIN SELECT unsafe_call13(); END; $$;

CREATE FUNCTION plpgsqlfunc16() RETURNS TEXT LANGUAGE PLPGSQL AS $$
BEGIN
  ASSERT true;
  SELECT unsafe_call17();
  SET search_path TO pg_catalog;
  SELECT safe_call19();
  RESET search_path;
  SELECT unsafe_call21();
  SELECT foo.safe_call22();
END;
$$;
