
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from ..domain import IHTMLConverter


class HTMLConverter(IHTMLConverter):

    def handle(self, raw, syntax):
        if syntax == 'plain':
            return raw
        return highlight(raw, get_lexer_by_name(syntax), HtmlFormatter())
