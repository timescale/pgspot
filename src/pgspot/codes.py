codes = {
    "PS001": {
        "title": "Unqualified operator",
        "description": """
        An operator was used with an unsafe search path, or not fully schema-qualified.

        Erroneous example:

        ```
        SELECT foo + bar;
        ```

        The `+` operator is used here without either a) setting the search path or
        b) fully-qualifying the operator.

        An attacker could create a custom `+` operator and redirect execution to
        their operator by either making their operator have better matching types
        or by modifying search_path so that an attacker-controlled schema is searched
        first.

        To mitigate, either
        a) explicitly set the search path:

        ```
        SET search_path = pg_catalog, pg_temp;
        SELECT foo + bar;
        ```

        or b) fully schema-qualify the operator

        ```
        SELECT foo OPERATOR(pg_catalog.+) bar;
        ```
        """,
    },
    "PS002": {
        "title": "Unsafe function creation",
        "description": """
        A function was created using `CREATE OR REPLACE` in an insecure schema.

        Erroneous example:

        ```
        CREATE OR REPLACE FUNCTION public.foo() RETURNS INTEGER LANGUAGE SQL AS $$SELECT 1;$$;
        ```

        Using `CREATE OR REPLACE` in a schema which is not owned by the extension is
        insecure. An attacker can pre-create the desired function, becoming owner of
        the function, and allowing them to later change the body of the function.

        To mitigate this issue, either

        a) Use `CREATE OR REPLACE FUNCTION` in an extension-owned schema:

        ```
        CREATE SCHEMA extension_schema;
        CREATE OR REPLACE FUNCTION extension_schema.foo() RETURNS INTEGER LANGUAGE SQL AS $$SELECT 1;$$;
        ```

        or b) use `CREATE FUNCTION` (without `OR REPLACE`):

        ```
        CREATE FUNCTION public.foo() RETURNS INTEGER LANGUAGE SQL AS $$SELECT 1;$$;
        ```

        PostgreSQL versions 14.5+, 13.8+, 12.12+, 11.17+ and 10.22+ will block the
        CREATE OR REPLACE in an extension script if the statement would replace an
        object not belonging to the extension which will prevent exploitation in an
        extension context.
        """,
    },
    "PS003": {
        "title": "SECURITY DEFINER function without explicit search_path",
        "description": """
        A function with `SECURITY DEFINER` was created without setting a fixed search path.

        Erroneous example:

        ```
        CREATE FUNCTION my_extension.security_definer_function()
            RETURNS VOID
            SECURITY DEFINER
            LANGUAGE SQL
        AS $$
            -- function body
        $$;
        ```

        In general, `SECURITY DEFINER` functions require extra care, as they are
        executed as a different user than the calling user, so can be abused for
        privilege escalation.

        In particular, it is highly advised to set a fixed, secure `search_path` for
        these functions, as it prevents a number of attacks which rely on an insecure
        `search_path`.

        To mitigate, set the `search_path` to the secure search path `pg_catalog, pg_temp`

        ```
        CREATE FUNCTION my_extension.security_definer_function()
            RETURNS VOID
            SECURITY DEFINER
            SET search_path = pg_catalog, pg_temp
            LANGUAGE SQL
        AS $$
            -- function body
        $$;
        ```
        """,
    },
    "PS004": {
        "title": "SECURITY DEFINER function with insecure search_path",
        "description": """
        A function with `SECURITY DEFINER` was created with an insecure search path.

        Erroneous example:

        ```
        CREATE FUNCTION my_extension.security_definer_function()
            RETURNS VOID
            SECURITY DEFINER
            SET search_path = public, pg_catalog
            LANGUAGE SQL
        AS $$
            -- function body
        $$;
        ```

        In general, `SECURITY DEFINER` functions require extra care, as they are
        executed as a different user than the calling user, so can be abused for
        privilege escalation.

        In particular, it is highly advised to set a fixed, secure `search_path` for
        these functions, as it prevents a number of attacks which rely on an insecure
        `search_path`.

        To mitigate, set the `search_path` to the secure search path `pg_catalog, pg_temp`

        ```
        CREATE FUNCTION my_extension.security_definer_function()
            RETURNS VOID
            SECURITY DEFINER
            SET search_path = pg_catalog, pg_temp
            LANGUAGE SQL
        AS $$
            -- function body
        $$;
        ```
        """,
    },
    "PS005": {
        "title": "Function without explicit search_path",
        "description": """
        A function was created without an explicit search_path defined.

        Erroneous example:

        ```
        CREATE FUNCTION my_extension.function()
            RETURNS VOID
            LANGUAGE SQL
        AS $$
            -- function body
        $$;
        ```

        In general, it is preferable to define an explicit search path for functions,
        as this can prevent insecure search_path attacks.

        To mitigate, set the `search_path` to the secure search path `pg_catalog, pg_temp`

        ```
        CREATE FUNCTION my_extension.function()
            RETURNS VOID
            SET search_path = pg_catalog, pg_temp
            LANGUAGE SQL
        AS $$
            -- function body
        $$;
        ```

        Note: There are legitimate cases in which it is not possible to set a fixed
        search path for a function (e.g. when it should be inlined, or participate in
        transactions). For this reason, PS005 is a warning, and can be ignored in those
        cases.
        """,
    },
    "PS006": {
        "title": "Unsafe transform creation",
        "description": """
        A transform was created using `CREATE OR REPLACE`.

        Erroneous example:

        ```
        CREATE OR REPLACE TRANSFORM rxid FOR LANGUAGE plpgsql(from sql with function f1);
        ```

        This warning is produced for consistency with all the other `CREATE OR REPLACE`
        statements. Currently this cannot be exploited to escalate privileges as the steps
        required to set this up require superuser privileges.

        To mitigate this issue, use `CREATE ...` (without `OR REPLACE`):

        ```
        CREATE TRANSFORM rxid FOR LANGUAGE plpgsql(from sql with function f1);
        ```

        PostgreSQL versions 14.5+, 13.8+, 12.12+, 11.17+ and 10.22+ will block the
        CREATE OR REPLACE in an extension script if the statement would replace an
        object not belonging to the extension which will prevent exploitation in an
        extension context.
        """,
    },
    "PS007": {
        "title": "Unsafe object creation",
        "description": """
        An object was created using `CREATE OR REPLACE` in an insecure schema.

        Erroneous example:

        ```
        CREATE OR REPLACE AGGREGATE public.aggregate(BASETYPE=my_type,SFUNC=agg_sfunc,STYPE=internal);
        ```

        Using `CREATE OR REPLACE` in a schema which is not owned by the extension is
        insecure. An attacker can pre-create the desired object, becoming owner of
        the object, and allowing them to later change attributes of object. This
        ultimately leads to malicious code execution.

        To mitigate this issue, either

        a) Use `CREATE OR REPLACE ...` in an extension-owned schema:

        ```
        CREATE SCHEMA extension_schema;
        CREATE OR REPLACE AGGREGATE extension_schema.aggregate(BASETYPE=my_type,SFUNC=agg_sfunc,STYPE=internal);
        ```

        or b) use `CREATE ...` (without `OR REPLACE`):

        ```
        CREATE AGGREGATE public.aggregate(SFUNC=agg_sfunc,STYPE=internal);
        ```

        PostgreSQL versions 14.5+, 13.8+, 12.12+, 11.17+ and 10.22+ will block the
        CREATE OR REPLACE in an extension script if the statement would replace an
        object not belonging to the extension which will prevent exploitation in an
        extension context.
        """,
    },
    "PS008": {
        "title": "Unqualified alter sequence",
        "description": """
        NOTE: This warning is not produced.
        """,
    },
    "PS009": {
        "title": "Unsafe CASE expression",
        "description": """
        A "simple" `CASE` expression was used without a secure search_path.

        Erroneous example:

        ```
        SELECT
            CASE a OPERATOR(pg_catalog.=) b
                WHEN true THEN 'true'
                WHEN false THEN 'false'
            END
        FROM my_schema.foo;
        ```

        The "simple" `CASE` expression evaluates an expression once, and then compares
        the result of that evaluation with the branches of the `CASE` expression. This
        comparison is performed with an equality operator which cannot be
        schema-qualified.

        To mitigate, either

        a) explicitly set the search path:

        ```
        SET search_path = pg_catalog, pg_temp;
        SELECT
            CASE a = b
                WHEN true THEN 'true'
                WHEN false THEN 'false'
            END
        FROM my_schema.foo;
        ```

        or b) use the alternate form of case expression:

        ```
        SELECT
            CASE
                WHEN a OPERATOR(pg_catalog.=) b THEN 'true'
                WHEN a OPERATOR(pg_catalog.!=) b THEN 'false'
            END
        FROM my_schema.foo;
        ```
        """,
    },
    "PS010": {
        "title": "Unsafe schema creation",
        "description": """
        A schema was created using `IF NOT EXISTS`.

        Erroneous example:

        ```
        CREATE SCHEMA IF NOT EXISTS my_schema;
        ```

        Using `IF NOT EXISTS` to create a schema means that the schema could have been
        pre-created by an attacker. As the attacker would own the schema, they would be
        able to modify arbitrary objects added to that schema by the extension. This
        allows for the execution of malicious code.

        To mitigate this issue use only `CREATE SCHEMA` without `IF NOT EXISTS`:

        ```
        CREATE SCHEMA my_schema;
        ```

        If the schema already exists when the extension is installed, then this
        statement will fail, which is desired behaviour.

        PostgreSQL versions 14.5+, 13.8+, 12.12+, 11.17+ and 10.22+ will block the
        CREATE IF NOT EXISTS in an extension script if the statement would replace an
        object not belonging to the extension which will prevent exploitation in an
        extension context.
        """,
    },
    "PS011": {
        "title": "Unsafe sequence creation",
        "description": """
        A sequence was created using `IF NOT EXISTS` in an insecure schema.

        Erroneous example:

        ```
        CREATE SEQUENCE IF NOT EXISTS public.s1;
        ```

        Using `CREATE ... IF NOT EXISTS` in a schema which is not owned by the
        extension is insecure. An attacker can pre-create the desired sequence, becoming
        owner of the sequence, allowing them to later modify attributes of the sequence
        and thereby controlling the values generated by the sequence.

        To mitigate this issue, either

        a) Use `CREATE SEQUENCE IF NOT EXISTS` in an extension-owned schema:

        ```
        CREATE SCHEMA extension_schema;
        CREATE SEQUENCE IF NOT EXISTS extension_schema.s1;
        ```

        or b) use `CREATE SEQUENCE` (without `IF NOT EXISTS`):

        ```
        CREATE SEQUENCE public.s1;
        ```

        PostgreSQL versions 14.5+, 13.8+, 12.12+, 11.17+ and 10.22+ will block the
        CREATE IF NOT EXISTS in an extension script if the statement would replace an
        object not belonging to the extension which will prevent exploitation in an
        extension context.
        """,
    },
    "PS012": {
        "title": "Unsafe table creation",
        "description": """
        A table was created using `IF NOT EXISTS` in an insecure schema.

        Erroneous example:

        ```
        CREATE TABLE IF NOT EXISTS public.test_table(col text);
        ```

        Using `CREATE ... IF NOT EXISTS` in a schema which is not owned by the
        extension is insecure. An attacker can pre-create the desired table, becoming
        owner of the table, allowing them to later modify attributes of the table. This
        ultimately leads to malicious code execution.

        To mitigate this issue, either

        a) Use `CREATE TABLE IF NOT EXISTS` in an extension-owned schema:

        ```
        CREATE SCHEMA extension_schema;
        CREATE TABLE IF NOT EXISTS extension_schema.test_table(col text);
        ```

        or b) use `CREATE TABLE` (without `IF NOT EXISTS`):

        ```
        CREATE TABLE public.test_table(col text);
        ```

        PostgreSQL versions 14.5+, 13.8+, 12.12+, 11.17+ and 10.22+ will block the
        CREATE IF NOT EXISTS in an extension script if the statement would replace an
        object not belonging to the extension which will prevent exploitation in an
        extension context.
        """,
    },
    "PS013": {
        "title": "Unsafe foreign server creation",
        "description": """
        A foreign server was created using `IF NOT EXISTS`.

        Erroneous example:

        ```
        CREATE SERVER IF NOT EXISTS s1 FOREIGN DATA WRAPPER postgres_fdw;
        ```

        Using `CREATE ... IF NOT EXISTS` is insecure. An attacker may pre-create
        the desired server, becoming owner of the server, allowing them to later
        modify attributes of the server. Since a user needs USAGE privilege on
        the FOREIGN DATA WRAPPER to create a server this might not be
        exploitable in most enviroments.

        To mitigate this issue, use `CREATE SERVER` (without `IF NOT EXISTS`):

        ```
        CREATE SERVER s1 FOREIGN DATA WRAPPER postgres_fdw;
        ```

        PostgreSQL versions 14.5+, 13.8+, 12.12+, 11.17+ and 10.22+ will block the
        CREATE IF NOT EXISTS in an extension script if the statement would replace an
        object not belonging to the extension which will prevent exploitation in an
        extension context.
        """,
    },
    "PS014": {
        "title": "Unsafe index creation",
        "description": """
        An index was created using `IF NOT EXISTS`.

        Erroneous example:

        ```
        CREATE INDEX IF NOT EXISTS i1 ON t(time);
        ```

        Using `CREATE ... IF NOT EXISTS` is insecure. An attacker can pre-create
        the index preventing the creation of unique constraints on the table.
        Indexes may also be used to execute malicious code.

        To mitigate this issue use `CREATE INDEX` (without `IF NOT EXISTS`):

        ```
        CREATE INDEX i1 ON t(time);
        ```
        """,
    },
    "PS015": {
        "title": "Unsafe view creation",
        "description": """
        A view was created using `CREATE OR REPLACE` in an insecure schema.

        Erroneous example:

        ```
        CREATE OR REPLACE VIEW public.test_view AS SELECT pg_catalog.now();
        ```

        Using `CREATE OR REPLACE` in a schema which is not owned by the extension is
        insecure. An attacker can pre-create the desired view, becoming owner of
        the view, allowing them to later modify the view. This ultimately leads to
        malicious code execution.

        To mitigate this issue, either

        a) Use `CREATE OR REPLACE VIEW` in an extension-owned schema:

        ```
        CREATE SCHEMA extension_schema;
        CREATE OR REPLACE VIEW extension_schema.test_view AS SELECT pg_catalog.now();
        ```

        or b) use `CREATE VIEW` (without `OR REPLACE`):

        ```
        CREATE VIEW public.test_view AS SELECT pg_catalog.now();
        ```

        PostgreSQL versions 14.5+, 13.8+, 12.12+, 11.17+ and 10.22+ will block the
        CREATE OR REPLACE in an extension script if the statement would replace an
        object not belonging to the extension which will prevent exploitation in an
        extension context.
        """,
    },
    "PS016": {
        "title": "Unqualified function call",
        "description": """
        A function was used with an unsafe search path, or not fully schema-qualified.

        Erroneous example:

        ```
        SELECT my_function(foo);
        ```

        The call to my_function was made without either a) setting the search path or
        b) fully schema-qualifying the function.

        An attacker could create a custom `my_function` function and redirect execution
        to their function by either making their function have better-matching types or
        by modifying the search_path so that an attacker-controlled schema is searched
        first.

        Either a) explicitly set the search path.

        ```
        SET search_path = pg_catalog, pg_temp;
        SELECT my_function(foo);
        ```

        or b) fully-qualify the function

        ```
        SELECT extension_schema.my_function(foo);
        ```
        """,
    },
    "PS017": {
        "title": "Unqualified object reference",
        "description": """
        An object was referenced with an unsafe search path, or not fully schema-qualified.

        Erroneous example:

        ```
        SELECT * FROM foo;
        ```

        The reference to `foo` was made without either a) setting the search path or
        b) fully schema-qualifying the relation.

        An attacker could create a temporary relation `foo`, or modify the search path
        so that an attacker-controlled relation is referenced instead of the desired.
        This could result in erroneous behaviour of a routine or function.

        To mitigate this, either a) explicitly set the search path:

        ```
        SET search_path = extension_schema;
        SELECT * FROM foo;
        ```

        or b) fully-qualify the object

        ```
        SELECT * FROM extension_schema.foo;
        ```
        """,
    },
}
