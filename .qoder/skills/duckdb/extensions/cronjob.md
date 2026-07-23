# cronjob extension

The DuckDB Cron extension adds support for scheduled query execution within DuckDB. It allows you to schedule SQL
queries to run periodically using standard cron expressions while your DuckDB process is active.

## Installing and Loading

```sql
INSTALL cronjob FROM community;
LOAD cronjob;
```

## Example

```
-- Every 15 seconds during hours 1-4
SELECT cron('SELECT now()', '*/15 * 1-4 * * *');

-- Every 2 hours (at minute 0, second 0) during hours 1-4
SELECT cron('SELECT version()', '0 0 */2 1-4 * *');

-- Every 5 minute (wipe old data)
SELECT cron('DELETE FROM somewhere WHERE ts < NOW() - INTERVAL ''1 hour''', '* /5 * * * *');

-- Inspect running Jobs
SELECT * FROM cron_jobs();

┌─────────┬──────────────────┬────────────────┬──────────────────────────┬─────────┬──────────────────────────┬─────────────┐
│ job_id  │      query       │    schedule    │         next_run         │ status  │         last_run         │ last_result │
│ varchar │     varchar      │    varchar     │         varchar          │ varchar │         varchar          │   varchar   │
├─────────┼──────────────────┼────────────────┼──────────────────────────┼─────────┼──────────────────────────┼─────────────┤
│ task_0  │ SELECT version() │ */15 * * * * * │ Fri Nov 15 20:44:30 2024 │ Active  │ Fri Nov 15 20:44:15 2024 │ Success     │
└─────────┴──────────────────┴────────────────┴──────────────────────────┴─────────┴──────────────────────────┴─────────────┘

-- Inspect running Jobs
SELECT cron_delete('task_0');

-- Supported Patterns
┌───────────── second (0 - 59)
│ ┌───────────── minute (0 - 59)
│ │ ┌───────────── hour (0 - 23)
│ │ │ ┌───────────── day of month (1 - 31)
│ │ │ │ ┌───────────── month (1 - 12)
│ │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │ │
* * * * * *

```

