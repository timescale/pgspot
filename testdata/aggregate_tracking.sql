
-- should warn twice
CREATE OR REPLACE AGGREGATE s1.agg3(int) (sfunc=abc);
CREATE OR REPLACE AGGREGATE s1.agg3(int) (sfunc=abc);

CREATE AGGREGATE s1.agg6(int) (sfunc=abc);
-- should not warn since it was previously created in this script
CREATE OR REPLACE AGGREGATE s1.agg6(int) (sfunc=abc);
-- different schema should warn
CREATE OR REPLACE AGGREGATE s2.agg6(int) (sfunc=abc);
-- should warn because no schema
CREATE OR REPLACE AGGREGATE agg6(int) (sfunc=abc);

-- different signature should warn
CREATE OR REPLACE AGGREGATE s1.agg6(int,int) (sfunc=abc);

-- old style
CREATE AGGREGATE s3.agg14 (BASETYPE=int,SFUNC=int4and,STYPE=int);
-- should not warn since it was previously created in this script
CREATE OR REPLACE AGGREGATE s3.agg14 (BASETYPE=int,SFUNC=int4and,STYPE=int);
-- should warn because of different basetype
CREATE OR REPLACE AGGREGATE s3.agg14 (BASETYPE=int8,SFUNC=int4and,STYPE=int);

-- new style with different signature should warn
CREATE OR REPLACE AGGREGATE s3.agg14(int8) (SFUNC=int4and,STYPE=int);

