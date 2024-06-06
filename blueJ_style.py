from collections.abc import Iterator
from typing import Iterable
from pygments.lexer import Lexer
from pygments.style import Style
from pygments.token import _TokenType, Token, Comment, Keyword, String, Name
from pygments.filter import Filter

class BlueJStyle(Style):

    styles = {
        Token:                  '#000000',
        Comment:                '#999999 bg:',
        Comment.Multiline:      '#000099 bg:',
        Keyword:                '#660134',
        String:                 '#066a06',
        Keyword.Type:           '#cd0b0a',
        Name.Builtin.Pseudo:    '#006699',
    }

class SpecialKeywordFilter(Filter):
    def __init__(self, **options):
        super().__init__(**options)
        self.special_keywords = {'null', 'this'}
    
    def filter(self, lexer, stream):
        for ttype, value in stream:
            if value in self.special_keywords:
                yield Name.Builtin.Pseudo, value
            else:
                yield ttype, value