create function public.fn() returns void
as $func$
declare
    _rec record;
begin
    for _rec in execute format
    ( $sql$
        select generate_series(%L, %L) as x
      $sql$
    , _catalog_id
    )
    loop
        raise notice '%', _rec.x;
        PERFORM format('%s', _rec.x);
    end loop;
end
$func$ language plpgsql volatile security invoker
;
