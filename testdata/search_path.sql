
-- should warn since its unqualified function call
SELECT unsafe_call3('%s','abc');
SELECT pg_catalog.safe_call4();

SET search_path TO pg_catalog, pg_temp;

-- safe since we have safe search_path now
SELECT safe_call9('%s','abc');
SELECT pg_catalog.safe_call10();

RESET search_path;

-- should warn since search_path got reset
SELECT unsafe_call15('%s','abc');
SELECT pg_catalog.safe_call16();

CREATE SCHEMA new;

SELECT new.safe_call20('%s','abc');
SELECT unsafe_call21('%s','abc');

