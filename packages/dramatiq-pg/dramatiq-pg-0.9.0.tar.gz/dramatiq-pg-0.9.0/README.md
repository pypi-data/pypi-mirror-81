![Dramatiq-pg](https://gitlab.com/dalibo/dramatiq-pg/raw/master/docs/logo-horizontal.png?inline=false)

[Dramatiq](https://dramatiq.io/) is a simple task queue implementation for
Python3. dramatiq-pg provides a Postgres-based implementation of a dramatiq
broker.


## Features

- Super simple deployment: Single table, no ORM.
- Stores message payload and results as native JSONb.
- Uses LISTEN/NOTIFY to keep worker sync. No polling.
- Implements delayed task.
- Reliable thanks to Postgres MVCC.
- Self-healing: automatic purge of old messages. Automatic recovery after
  crash.
- Utility CLI for maintainance: flush, purge, stats, etc.

Note that dramatiq assumes tasks are idempotent. This broker makes the same
assumptions for recovering after a crash.


## Installation

- Install dramatiq-pg package from PyPI:
  ``` console
  $ pip install dramatiq-pg psycopg2-binary
  ```
  Ensure you have either psycopg2 or psycopg2-binary installed.
- Init database schema with `init` command.
  ``` console
  $ dramatiq-pg init
  ```
  Or adapt `dramatiq-pg/schema.sql` to your needs.
- Before importing actors, define global broker with a connection
  pool:
  ``` python
  import dramatiq
  import psycopg2.pool
  from dramatiq_pg import PostgresBroker

  dramatiq.set_broker(PostgresBroker(i))

  @dramatiq.actor
  def myactor():
      ...
  ```

Now declare/import actors and manage worker just like any [dramatiq
setup](https://dramatiq.io/guide.html). An [example
script](https://gitlab.com/dalibo/dramatiq-pg/blob/master/example.py) is
available, tested on CI.

The CLI tool `dramatiq-pg` allows you to requeue messages, purge old messages
and show stats on the queue. See `--help` for details.

[Dramatiq-pg
documentation](https://gitlab.com/dalibo/dramatiq-pg/blob/master/docs/index.rst)
is hosted on GitLab and give you more details on deployment and operation of
Postgres as a Dramatiq broker.


## Integration

**Django** : Use
[django-dramatiq-pg](https://github.com/uptick/django-dramatiq-pg/) by [Curtis
Maloney](https://gitlab.com/FunkyBob). It includes configuration, ORM model and
database migration.


## Support

If you encounter a bug or miss a feature, please [open an issue on
GitLab](https://gitlab.com/dalibo/dramatiq-pg/issues/new) with as much
information as possible.

dramatiq_pg is available under the PostgreSQL licence.


## Credit

Thanks to all contributors :

- Andy Freeland
- Curtis Maloney, Django support.
- Federico Caselli, bugfixes.
- Giuseppe Papallo, bugfixes.
- Rafal Kwasny, improvements.


The logo is a creation of [Damien CAZEILS](http://www.damiencazeils.com/)
