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
        SET search_path = pg_catalog;
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
        
        To mitigate, set the `search_path` to the secure search path `pg_catalog`
        
        ```
        CREATE FUNCTION my_extension.security_definer_function()
            RETURNS VOID
            SECURITY DEFINER
            SET search_path = pg_catalog
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
        
        To mitigate, set the `search_path` to the secure search path `pg_catalog`
        
        ```
        CREATE FUNCTION my_extension.security_definer_function()
            RETURNS VOID
            SECURITY DEFINER
            SET search_path = pg_catalog
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
        
        To mitigate, set the `search_path` to the secure search path `pg_catalog`
        
        ```
        CREATE FUNCTION my_extension.function()
            RETURNS VOID
            SET search_path = pg_catalog
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
        TODO
        """,
    },
    "PS007": {
        "title": "Unsafe object creation",
        "description": """
        TODO
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
        SET search_path = pg_catalog;
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
        """,
    },
    "PS011": {
        "title": "Unsafe sequence creation",
        "description": """
        TODO
        """,
    },
    "PS012": {
        "title": "Unsafe table creation",
        "description": """
        TODO
        """,
    },
    "PS013": {
        "title": "Unsafe foreign server creation",
        "description": """
        TODO
        """,
    },
    "PS014": {
        "title": "Unsafe index creation",
        "description": """
        TODO
        """,
    },
    "PS015": {
        "title": "Unsafe view creation",
        "description": """
        TODO
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
        SET search_path = pg_catalog;
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
