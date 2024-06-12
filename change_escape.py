import functools
from pygments.formatters import HtmlFormatter

anti_escape_html_table = {
    ord('&'): '&',
    ord('<'): '<',
    ord('>'): '>',
    ord('"'): '"',
    ord("'"): "'",
}

class HtmlFormatterSpecialEscape(HtmlFormatter):
    @functools.lru_cache(maxsize=100)
    def _translate_parts(self, value):
        """old : HTML-escape a value and split it by newlines."""
        return value.translate(anti_escape_html_table).split('\n')