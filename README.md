## pgspot

Spot vulnerabilities in extension update scripts.

### Usage

```
pgspot <<<"CREATE TABLE IF NOT EXISTS foo();"
Unsafe table creation: foo
Unqualified object reference: foo

Errors: 1 Warnings: 1 Unknown: 0
```

