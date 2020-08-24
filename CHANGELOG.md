# CHANGELOG

## v0.0.4 (August XX, 2020)

- Fixes.
- TraktorConfig accepts config file location. Needed for application that
  will reuse it's configuration structure but in another file, like
  `traktor-server`.


---


## v0.0.3 (August 23, 2020)

- Fix broken json output.
- List all tasks without specifying the project.
- Database export to json file.
- Database load from json file.
- Timer commands are now top level commands.
- Add support for switching between test and production database.
- Add interactive status.
- HTTP API added.
- Client for the HTTP API created.
- Rewrite in django.
- Admin interface added.
- Client is synchronous now.
- Extract server component to traktor-server project.


---


## v0.0.2 (August 09, 2020)

- Fix missing alembic migrations in he package.
- Add default task option. If the task is not provider on timer start the
  default task will be used.
- Refactor.


---


## v0.0.1 (August 09, 2020)

- Initial beta release. 
