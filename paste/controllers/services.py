from paste.application.html_converter import HTMLConverter
from paste.application.repositories import SnippetRepository, UserRepository
from paste.domain import SnippetService, UserService

user_service = UserService(UserRepository())
snippet_service = SnippetService(HTMLConverter(), SnippetRepository())
