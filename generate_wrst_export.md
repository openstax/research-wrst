# Connect to database associated with wrst
`heroku pg:psql --app wrst-stage`

To see all the tables in the database
`\dt`

Export all data

`\COPY users TO '~/Desktop/kg_user_export.csv' WITH (FORMAT csv, DELIMITER ',',  HEADER true);`
`\COPY relationships TO '~/Desktop/kg_relationship_export.csv' WITH (FORMAT csv, DELIMITER ',',  HEADER true);`

Export specif query
`\COPY (SELECT * FROM relationships WHERE family = 'spatial') TO '~/Desktop/kg_relation_query_export.csv' WITH (FORMAT csv, DELIMITER ',',  HEADER true);`

To check table schema
`\d users`

To clear table
`DELETE FROM table_name;`

To count the number of unique paragraph ids
`SELECT COUNT(DISTINCT(paragraph_id)) FROM relationships;`

## Reference:
https://jamesbedont.com/export-a-heroku-postgres-table-to-a-csv-file
https://thoughtbot.com/blog/psql-basics
https://www.postgresql.org/docs/8.2/sql-delete.html