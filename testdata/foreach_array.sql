DO LANGUAGE plpgsql $$
DECLARE
    desired_roles text[] := '{pg_checkpoint,pg_signal_backend,pg_read_all_stats,pg_stat_scan_tables}';
    desired_role text;
BEGIN
    FOREACH desired_role IN ARRAY desired_roles LOOP
        IF pg_catalog.to_regrole(desired_role) IS NOT NULL THEN
            EXECUTE format('GRANT %I TO tsdbadmin', desired_role);
        END IF;
    END LOOP;
END;
$$;
