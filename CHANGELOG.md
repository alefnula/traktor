# CHANGELOG


## v0.0.10 (September 02, 2020)

- `tea-console` and `tea-django` update.


---


## v0.0.9 (September 02, 2020)

- Django admin fixes.
- Add user field to Report model.


---


## v0.0.8 (August 28, 2020)

- Misplaced stuff fix.


---


## v0.0.7 (August 28, 2020)

- Add user model and tie projects to user.
- Prefetch related task and project on Task and Entry to generate less SQL
  queries.
- Default task creation on project creation.


---


## v0.0.6 (August 24, 2020)

- Fixing requirements.


---


## v0.0.5 (August 24, 2020)

- Updated requirements.


---


## v0.0.4 (August 24, 2020)

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
