"""
Application specific layer
"""

from collections import defaultdict

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from .domain import IHTMLConverter, IRepository, Snippet, User


class UserRepository(IRepository):

    # indexes
    _users_by_pk = {}
    _users_by_name = {}
    _users_by_auth = {}

    def save(self, user: User) -> User:
        if user.pk is None:
            user.pk = len(self._users_by_pk) + 1

        self._users_by_pk[user.pk] = user
        self._users_by_name[user.name] = user
        self._users_by_auth[user.name + user.passhash] = user

        return user

    def get(self, **kw) -> User:
        if 'pk' in kw:
            return self._users_by_pk[kw['pk']]

        if 'passhash' not in kw:
            return self._users_by_name[kw['name']]

        return self._users_by_auth[kw['name'] + kw['passhash']]

    def filter(self, page: int, size: int, **kw) -> [User]:
        return self._users_by_pk.values()


class SnippetRepository(IRepository):

    # indexes
    _snippets_by_pk = {}
    _snippets_by_author = defaultdict(list)

    def save(self, snippet: Snippet):
        if snippet.pk is None:
            snippet.pk = len(self._snippets_by_pk) + 1

        self._snippets_by_pk[snippet.pk] = snippet

        if snippet.author is not None:
            self._snippets_by_author[snippet.author.pk].append(snippet)

        return snippet

    def get(self, **kw) -> Snippet:
        return self._snippets_by_pk[kw['pk']]

    def filter(self, page: int, size: int, **kw) -> [Snippet]:
        author = kw.get('author')
        to_index = page * size
        from_index = to_index - size

        if author is None:
            snippets = list(self._snippets_by_pk.values())
        else:
            snippets = self._snippets_by_author[author.pk]

        snippets.sort(key=lambda x: x.created_at, reverse=True)
        return snippets[from_index:to_index]


class HTMLConverter(IHTMLConverter):

    def handle(self, raw: str, syntax: str) -> str:
        if syntax == 'plain':
            return raw
        return highlight(raw, get_lexer_by_name(syntax), HtmlFormatter())
