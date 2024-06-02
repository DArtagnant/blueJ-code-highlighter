from pygments.style import Style
from pygments.token import Token, Comment, Keyword, String, Name
from pygments.filters import NameHighlightFilter

class BlueJStyle(Style):

    styles = {
        Token:                  '#000000',
        Comment:                '#999999 bg:',
        Comment.Multiline:      '#000099 bg:',
        Keyword:                '#660134',
        String:                 '#066a06',
        Keyword.Type:           '#cd0b0a',
        Name.Builtin.Pseudo:    '#1B00FF',
    }

specialKeywordFilter = NameHighlightFilter(
    names= ['this', 'null'],
    tokentype= Name.Builtin.Pseudo
)