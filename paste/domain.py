"""
Domain specific layer
"""

import datetime as dt
import hashlib


class Entity:

    attrs = {
        'pk': int,
        'created_at': dt.datetime,
    }

    def __init__(self, **kw):
        for k in self.attrs:
            setattr(self, k, None)

        for k, v in kw.items():
            if k not in self.attrs:
                raise AttributeError(k)

            if v is not None and not isinstance(v, self.attrs[k]):
                raise TypeError('%r is not %r' % (v, self.attrs[k]))

            setattr(self, k, v)


class User(Entity):

    attrs = dict({
        'name': str,
        'password': str,
        'passhash': str,
    }, **Entity.attrs)


class Snippet(Entity):

    attrs = dict({
        'raw': str,
        'syntax': str,
        'name': str,
        'author': User,
        'html': str,
    }, **Entity.attrs)


class IRepository:

    def save(self, entity: Entity) -> Entity:
        raise NotImplementedError

    def get(self, **kw) -> Entity:
        raise NotImplementedError

    def filter(self, page: int, size: int, **kw) -> [Entity]:
        raise NotImplementedError


class IHTMLConverter:

    def handle(self, raw: str, syntax: str) -> str:
        raise NotImplementedError


class Service:

    def __init__(self, repository: IRepository):
        self._repository = repository

    def get_by_pk(self, pk: int) -> Entity:
        return self._get(pk=pk)

    def _get(self, **kw) -> Entity:
        return self._repository.get(**kw)

    def _filter(self, **kw) -> Entity:
        return self._repository.filter(**kw)

    def _create(self, entity: Entity) -> Entity:
        entity.created_at = dt.datetime.utcnow()
        return self._repository.save(entity)


class UserService(Service):

    def register(self, user: User) -> User:
        user.passhash = get_hash(user.password)
        return self._create(user)

    def auth(self, name: str, password: str) -> User:
        return self._get(name=name, passhash=get_hash(password))

    def get_by_name(self, name: str) -> User:
        return self._get(name=name)


class SnippetService(Service):

    def __init__(self, converter: IHTMLConverter, *args, **kw):
        super().__init__(*args, **kw)
        self._converter = converter

    def filter(
        self, page: int=1, size: int=20, author: User=None,
    ) -> [Snippet]:
        return self._filter(page=page, size=size, author=author)

    def create(self, snippet: Snippet) -> Snippet:
        snippet.html = self._converter.handle(
            snippet.raw, snippet.syntax,
        )
        return self._create(snippet)


def get_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()
