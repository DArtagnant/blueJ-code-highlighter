import functools
from pygments.formatters import HtmlFormatter

class HtmlFormatterSpecialEscape(HtmlFormatter):
    #We disable this function
    @functools.lru_cache(maxsize=100)
    def _translate_parts(self, value):
        """old : HTML-escape a value and split it by newlines."""
        return value.split('\n')