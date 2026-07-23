# shellfs  extension

Allow shell commands to be used for input and output

## Installing and Loading

```sql
INSTALL shellfs FROM community;
LOAD shellfs;
```

## Example

```sql

-- create macro for osqueryi
CREATE OR REPLACE MACRO osquery(table_name) AS TABLE
    SELECT *FROM read_csv('/usr/local/bin/osqueryi "select * from ' || table_name || '" --csv --separator "," |');

-- query osquery's table
select * from osquery('processes');
```