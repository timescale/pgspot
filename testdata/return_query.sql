
create function ret_query() returns table(y int)
as $func$
declare
  a text;
  b text;
begin
    return query execute $$select format('abc',1,2)::int$$;
    return query execute $$select format('abc',$1,2)::int$$ using a;
    return query execute b;
    return query execute b || b;
end;
$func$ language plpgsql;

