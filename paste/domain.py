"""
Domain specific layer
"""

import hashlib


class DoesNotExist(Exception):
    pass


class Entity:

    def __init__(self, pk=None, created_at=None, updated_at=None):
        self.pk = pk
        self.created_at = created_at
        self.updated_at = updated_at


class User(Entity):

    def __init__(self, name, password=None, passhash=None, **kw):
        super().__init__(**kw)
        self.name = name
        self.password = password
        self.passhash = passhash


class Snippet(Entity):

    def __init__(self, raw, syntax, html=None, name=None, author=None, **kw):
        super().__init__(**kw)
        self.raw = raw
        self.syntax = syntax
        self.name = name
        self.author = author
        self.html = html


class IRepository:

    def count(self) -> int:
        raise NotImplementedError

    def save(self, entity: Entity) -> Entity:
        raise NotImplementedError

    def get(self, **kw) -> Entity:
        """
        raise DoesNotExist if object not founded
        """
        raise NotImplementedError

    def find(self, page: int, size: int, **kw) -> [Entity]:
        raise NotImplementedError


class IHTMLConverter:

    def handle(self, raw: str, syntax: str) -> str:
        raise NotImplementedError


class Service:

    def __init__(self, repository):
        self._repository = repository

    def get_by_pk(self, pk):
        return self._get(pk=pk)

    def _get(self, **kw):
        return self._repository.get(**kw)

    def _find(self, **kw):
        return self._repository.find(**kw)

    def _create(self, entity):
        return self._repository.save(entity)


class UserService(Service):

    def register(self, user):
        user.passhash = get_hash(user.password)
        return self._create(user)

    def auth(self, name, password):
        return self._get(name=name, passhash=get_hash(password))

    def get_by_name(self, name):
        return self._get(name=name)


class SnippetService(Service):

    def __init__(self, converter, *args, **kw):
        super().__init__(*args, **kw)
        self._converter = converter

    def get_page(self, page=1, size=20, author=None):
        query = {'page': page, 'size': size}
        if author is not None:
            query['author'] = author
        return self._find(**query)

    def create(self, snippet):
        snippet.html = self._converter.handle(snippet.raw, snippet.syntax)
        return self._create(snippet)


def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()
