"""
Migration '0001_initial.py'
Created at 2016-12-09T15:15:28.921328
"""

from playhouse.migrate import SqliteDatabase, SqliteMigrator, migrate

from paste import settings  # noqa
from paste.application.db import Snippet, User  # noqa


def apply():
    database = SqliteDatabase(settings.DATABASE)
    migrator = SqliteMigrator(database)

    with database.transaction():
        database.execute_sql('CREATE TABLE user (pk INTEGER PRIMARY KEY)')
        database.execute_sql('CREATE TABLE snippet (pk INTEGER PRIMARY KEY)')

        for field in (
            User.created_at,
            User.updated_at,
            User.name,
            User.passhash,
            Snippet.created_at,
            Snippet.updated_at,
            Snippet.syntax,
            Snippet.raw,
            Snippet.html,
        ):
            field.null = True

        migrate(
            # user table
            migrator.add_column('user', 'created_at', User.created_at),
            migrator.add_column('user', 'updated_at', User.updated_at),
            migrator.add_column('user', 'name', User.name),
            migrator.add_column('user', 'passhash', User.passhash),
            migrator.add_index('user', ('name', ), True),
            migrator.add_index('user', ('updated_at', ), False),

            # snippet table
            migrator.add_column('snippet', 'created_at', Snippet.created_at),
            migrator.add_column('snippet', 'updated_at', Snippet.updated_at),
            migrator.add_column('snippet', 'author_id', Snippet.author),
            migrator.add_column('snippet', 'name', Snippet.name),
            migrator.add_column('snippet', 'syntax', Snippet.syntax),
            migrator.add_column('snippet', 'raw', Snippet.raw),
            migrator.add_column('snippet', 'html', Snippet.html),
            migrator.add_index('snippet', ('updated_at', ), False),
        )


def rollback():
    database = SqliteDatabase(settings.DATABASE)
    with database.transaction():
        database.execute_sql('DROP TABLE user')
        database.execute_sql('DROP TABLE snippet')
