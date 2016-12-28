
import peewee

from .. import settings

database = peewee.SqliteDatabase(
    settings.DATABASE, threadlocals=True, autocommit=True, journal_mode='WAL',
)


class AbstractModel(peewee.Model):

    pk = peewee.PrimaryKeyField()
    created_at = peewee.DateTimeField()
    updated_at = peewee.DateTimeField(index=True)

    class Meta:
        database = database
        order_by = ('-updated_at', )


class User(AbstractModel):

    name = peewee.CharField(unique=True)
    passhash = peewee.CharField()


class Snippet(AbstractModel):

    author = peewee.ForeignKeyField(User, null=True)
    name = peewee.CharField(null=True)
    syntax = peewee.CharField()
    raw = peewee.TextField()
    html = peewee.TextField()
