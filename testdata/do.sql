
DO LANGUAGE PLPGSQL $$ BEGIN SELECT unsafe_call2(); END; $$;
DO LANGUAGE PLPGSQL $$ BEGIN PERFORM unsafe_call3(); END; $$;

-- nested DO
DO LANGUAGE PLPGSQL $$
BEGIN
  PERFORM unsafe_call8();
  DO $i$
  BEGIN
    PERFORM unsafe_call10();
  END;
  $i$;
  SET search_path TO pg_catalog,pg_temp;
  DO $i$
  BEGIN
    PERFORM safe_call17();
    RESET search_path;
    PERFORM unsafe_call19();
  END;
  $i$;
END;
$$;

-- unknown language
DO LANGUAGE PLLUA $$
  print("Hello World")
$$;

