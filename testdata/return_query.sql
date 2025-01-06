
create function ret_query() returns table(y int)
as $func$
declare
  a text;
begin
    return query execute $$select format('abc',1,2)::int$$;
    return query execute a;
    return query execute a + 'def';
end;
$func$ language plpgsql;

