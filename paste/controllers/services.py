from ..application.html_converter import HTMLConverter
from ..application.repositories import SnippetRepository, UserRepository
from ..domain import SnippetService, UserService

user_service = UserService(UserRepository())
snippet_service = SnippetService(HTMLConverter(), SnippetRepository())
