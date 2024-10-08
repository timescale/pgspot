create or replace function w1() returns void as $func$
declare
	_count bigint;
begin
	select 100 into strict _count;
	while format1('%s','false')::bool loop
	end loop;
	while 0 < _count loop
		_count := _count - 1;
    PERFORM format2('%s','true');
	end loop;
end
$func$ language plpgsql;
