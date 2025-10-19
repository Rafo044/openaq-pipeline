ALTER SYSTEM SET logging_collector = on;
ALTER SYSTEM SET log_directory = 'pg_log';
ALTER SYSTEM SET log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log';
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET archive_mode = 'ON';

ALTER SYSTEM SET archive_command = 'pgbackrest --stanza=main archive-push %p'
ALTER SYSTEM SET restore_command = 'pgbackrest --stanza=main archive-get %f %p'

SELECT pg_reload_conf();
