# PgDont

PgDont help to quickly check a database against the ["Don't Do This"](https://wiki.postgresql.org/wiki/Don't_Do_This). It's more of an audit tool than a linter, but it alse can be use this way.


## Usage

```shell
pgdont --dsn "host=localhost dbname=mydb user=john password=pass"
```

## Implemented rules

PgDont will check for the followings bad practices :


- [x] Upper case table name
- [x] Upper case column name
- [x] Use of 'SQL_ASCII' encoding
- [x] Use of Postgres Rules
- [x] Use of inherited tables

...


## Todo

- [ ] Implement missing rules
- [ ] Add config file 
- [ ] Manage multi-schema
- [ ] Cleaner output summary
