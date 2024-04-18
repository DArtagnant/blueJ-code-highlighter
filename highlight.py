from pygments import format
from pygments.lexers.jvm import JavaLexer
from pygments.formatters import HtmlFormatter
from pygments.token import Token

from blueJ_style import BlueJStyle

def nextNoSpaceToken(tokens, index):
    try:
        nextTokenType, nextTokenValue = tokens[index + 1]
        if nextTokenType is not Token.Text.Whitespace:
            return nextTokenType, nextTokenValue, index + 1
        else:
            return nextNoSpaceToken(tokens, index + 1)
    except IndexError:
        return None, None, None

def reformat(string_format):
    string_format = string_format.replace('<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%;"><span></span>', '')
    string_format = string_format.replace('</pre></div>\n', '')
    return string_format

def iter_to_string(iter):
    s = ""
    for i in iter:
        s += i[1]
    return s

Zones = {
    "outside" : "o",
    "classHeader" : "ch",
    "classBody" : "cb",
    "funHeader" : "fh",
    "funBody" : "fb",
}

def parseFromToken(tokens):
    htmlResult = ""
    zone = Zones["outside"]
    after_enter = False
    changed_before = False
    depth = 0

    actualIter = []
    for index, (tokenType, tokenValue) in enumerate(tokens):
        future_zone = zone

        if after_enter:
            after_enter = False
            if all(car == " " for car in tokenValue):
                continue
        if changed_before:
            changed_before = False
            if tokenValue == "\n":
                after_enter = True
                continue
        
        if tokenValue == "\n":
            after_enter = True
        
        if tokenType is Token.Comment.Multiline:
            nextTokenType, nextTokenValue, index1 = nextNoSpaceToken(tokens, index)
            if (nextTokenType is Token.Keyword.Declaration and
                (nextTokenValue == 'public' or nextTokenValue == 'private')):
                next2TokenType, next2TokenValue, index2 = nextNoSpaceToken(tokens, index1)
                if (next2TokenType is Token.Keyword.Declaration and
                    next2TokenValue == 'class'):
                    future_zone = Zones["classHeader"]
                else:
                    future_zone = Zones["funHeader"]
                htmlResult += htmlFromIter(actualIter, zone)
                actualIter.clear()
                changed_before = True
        elif (tokenType is Token.Keyword.Declaration and
            (tokenValue == 'public' or tokenValue == 'private')):
            nextTokenType, nextTokenValue, index1 = nextNoSpaceToken(tokens, index)
            if (nextTokenType is Token.Keyword.Declaration and
                nextTokenValue == 'class'):
                future_zone = Zones["classHeader"]
            else:
                future_zone = Zones["funHeader"]
            htmlResult += htmlFromIter(actualIter, zone)
            actualIter.clear()
            changed_before = True
        
        if (tokenType is Token.Punctuation and
            tokenValue == "}"):
            htmlResult += htmlFromIter(actualIter, zone)
            actualIter.clear()
            if depth == 2:
                future_zone = Zones["classBody"]
                htmlResult += htmlFromIter([(tokenType, tokenValue)], Zones['funHeader'])
            elif depth == 1:
                future_zone = Zones["outside"]
                htmlResult += htmlFromIter([(tokenType, tokenValue)], Zones['classHeader'])
            depth -= 1
            changed_before = True
            zone = future_zone
            continue
        
        if tokenType is Token.Comment.Multiline:
            lines = tokenValue.split("\n")
            lines = [line.strip() for line in lines]
            tokenValue = "\n".join(lines)
        actualIter.append((tokenType, tokenValue))

        if (tokenType is Token.Punctuation and
            tokenValue == "{"):
            depth += 1
            if depth > 2:
                print("WARNING: operation may be incorrect with depths greater than 2")
            if zone == Zones["funHeader"]:
                future_zone = Zones["funBody"]
            elif zone == Zones["classHeader"]:
                future_zone = Zones["classBody"]
            htmlResult += htmlFromIter(actualIter, zone)
            actualIter.clear()
            changed_before = True
        
        zone = future_zone
        
    htmlResult = '<pre>' + htmlResult + '</pre>'
    return htmlResult


def htmlFromIter(iter, zone):
    formatted_html = ""
    if zone == Zones["classHeader"]:
        formatted_html += '<div style="background-color: #e1f8e1;">'
    elif zone == Zones["classBody"]:
        formatted_html += '<div style="border-left: 25px solid #e1f8e1;">'
    elif zone == Zones["funHeader"]:
        formatted_html += '<div style="border-left: 25px solid #e1f8e1;"><div style="background-color: #fafab4;">'
    elif zone == Zones["funBody"]:
        formatted_html += '<div style="border-left: 25px solid #e1f8e1;"><div style="border-left: 25px solid #fafab4;">'
    elif zone == Zones["outside"]:
        pass
    else:
        raise Exception("'zone' non-valid value")
    formatted_html += reformat(format(iter, formatter))
    if zone == Zones["classHeader"] or zone == Zones["classBody"]:
        formatted_html += '</div>'
    elif zone == Zones["funHeader"] or zone == Zones["funBody"]:
        formatted_html += '</div></div>'
    elif zone == Zones["outside"]:
        pass
    return formatted_html

if __name__ == "__main__":
    code = ""
    with open("input.txt", "r") as file:
        code = file.read()
    
    lexer = JavaLexer()
    formatter = HtmlFormatter(noclasses=True, style=BlueJStyle)
    tokens = list(lexer.get_tokens(code))
    result_html = parseFromToken(tokens)

    with open("output.html", 'w') as file:
        file.write(result_html)