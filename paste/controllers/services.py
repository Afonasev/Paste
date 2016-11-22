from ..application import SnippetRepository, HTMLConverter, UserRepository
from ..domain import SnippetService, UserService

user_service = UserService(UserRepository())
snippet_service = SnippetService(HTMLConverter(), SnippetRepository())
