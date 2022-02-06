-- test OR REPLACE for various create statements

CREATE OR REPLACE AGGREGATE unsafe_agg3(SFUNC=agg_sfunc,STYPE=internal);
CREATE OR REPLACE FUNCTION unsafe_func4() RETURNS TEXT LANGUAGE SQL AS $$ SELECT '123'; $$;
CREATE OR REPLACE PROCEDURE unsafe_proc5() LANGUAGE SQL AS $$ SELECT '123'; $$;
CREATE OR REPLACE TRANSFORM FOR type6 LANGUAGE lang6 (FROM SQL WITH FUNCTION hstore_to_plpython(internal), TO SQL WITH FUNCTION plpython_to_hstore(internal));
-- this is pg14 only which is not yet supported by sql parser
-- CREATE OR REPLACE TRIGGER trigger8 BEFORE INSERT ON table8 FOR EACH ROW EXECUTE PROCEDURE proc8();
CREATE OR REPLACE VIEW view9 AS SELECT pg_catalog.now();

