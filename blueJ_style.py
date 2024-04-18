from pygments.style import Style
from pygments.token import Token, Comment, Keyword, String

class BlueJStyle(Style):

    styles = {
        Token:                  '#000000',
        Comment:                '#999999 bg:#ffffff',
        Comment.Multiline:      '#000099 bg:',
        Keyword:                '#660134',
        String:                 '#066a06',
        Keyword.Type:           '#cd0b0a'
    }