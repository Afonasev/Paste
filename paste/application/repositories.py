from datetime import datetime

import peewee

from . import db
from .. import domain


class AbstractRepository(domain.IRepository):

    _model = NotImplemented
    _entity = NotImplemented

    def count(self):
        return self._model.count()

    def save(self, entity):
        model = _entity_to_model(entity)

        if model.pk is None:
            model.created_at = datetime.utcnow()

        model.updated_at = datetime.utcnow()
        model.save()

        return _model_to_entity(model)

    def get(self, **kw):
        try:
            return _model_to_entity(self._model.get(**kw))
        except peewee.DoesNotExist:
            raise domain.DoesNotExist('%s: %s' % (self._entity, kw))

    def find(self, page, size, **kw):
        if kw:
            for k, v in kw.items():
                if isinstance(v, domain.Entity):
                    kw[k] = v.pk
            query = self._model.filter(**kw)
        else:
            query = self._model.select()

        return [_model_to_entity(i) for i in query.paginate(page, size)]

    def delete(self, entity):
        _entity_to_model(entity).delete_instance()


class UserRepository(AbstractRepository):

    _model = db.User
    _entity = domain.User


class SnippetRepository(AbstractRepository):

    _model = db.Snippet
    _entity = domain.Snippet


def _by_object(obj):
    name = obj.__class__.__name__
    fields = ('pk', 'created_at', 'updated_at')

    if name == 'User':
        return domain.User, db.User, fields + ('name', 'passhash')

    if name == 'Snippet':
        fields += ('author', 'name', 'syntax', 'raw', 'html')
        return domain.Snippet, db.Snippet, fields

    raise NotImplementedError


def _entity_to_model(entity):
    _, model_cls, fields = _by_object(entity)
    attrs = {}
    for field in fields:
        value = getattr(entity, field)
        if isinstance(value, domain.Entity):
            value = value.pk
        attrs[field] = value
    return model_cls(**attrs)


def _model_to_entity(model):
    entity_cls, _, fields = _by_object(model)
    attrs = {}
    for f in fields:
        value = getattr(model, f)
        if isinstance(value, db.AbstractModel):
            value = _model_to_entity(value)
        attrs[f] = value
    return entity_cls(**attrs)
