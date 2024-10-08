create or replace function l() returns void as $func$
declare
begin
 	loop
 	end loop;
 	loop
 		PERFORM f1('select 1');
    exit when f2();
 	end loop;
end
$func$ language plpgsql;
