
DO LANGUAGE PLPGSQL $$ BEGIN SELECT unsafe_call2(); END; $$;
DO LANGUAGE PLPGSQL $$ BEGIN PERFORM unsafe_call3(); END; $$;
