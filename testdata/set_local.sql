
SET search_path TO pg_catalog;

-- safe since search_path is locked down
SELECT safe_call5();

COMMIT;

-- safe since search_path is still locked down
SELECT safe_call10();

RESET search_path;

BEGIN;
SET LOCAL search_path TO pg_catalog;
-- safe since search_path is still locked down
SELECT safe_call17();
COMMIT;

-- unsafe since rollback ended SET LOCAL
SELECT unsafe_call21();

BEGIN;
SET LOCAL search_path TO pg_catalog;
-- safe since search_path is still locked down
SELECT safe_call26();
ROLLBACK;

-- unsafe since rollback ended SET LOCAL
SELECT unsafe_call30();

