from pygments.style import Style
from pygments.token import Token, Comment, Keyword, Name, String, \
Error, Generic, Number, Operator


class BlueJStyle(Style):

    styles = {
        Token:                  '',
        Comment:                'ansigray',
        Comment.Multiline:      'ansiblue',
        Keyword:                'ansimagenta',
        Keyword.Reserved:       'ansiyellow'
    }