from pygments import format
from pygments.lexers.jvm import JavaLexer
from pygments.formatters import HtmlFormatter
from pygments.token import Token
from re import sub as re_sub
from re import MULTILINE as re_m_flag

from enum import Enum, auto
from blueJ_style import BlueJStyle, SpecialKeywordFilter


java_memory_protection = {'public', 'private', 'protected'}
java_memory_conditions = {'if', 'else'}
java_memory_loops = {'for', 'while'}
java_memory_special = {'class', ';', '}', '{'}
java_memory_all_keywords = (
      java_memory_protection
    | java_memory_conditions
    | java_memory_loops
    | java_memory_special
)

class Zones(Enum):
    outside = auto()
    classHeader = auto()
    classBody = auto()
    funHeader = auto()
    funBody = auto()
    otherHeader = auto()
    otherBody = auto()

    @property
    def logicalFollower(self):
        match self:
            case Zones.outside: return Zones.outside
            case Zones.classHeader: return Zones.classBody
            case Zones.classBody: return Zones.classBody
            case Zones.funHeader: return Zones.funBody
            case Zones.funBody: return Zones.funBody
            case Zones.otherHeader: return Zones.otherBody
            case Zones.otherBody: return Zones.otherBody
            case _: raise Exception("'zone' non-valid value") 
    
    @property
    def logicalPreceding(self):
        match self:
            case Zones.outside: return Zones.outside
            case Zones.classHeader: return Zones.classHeader
            case Zones.classBody: return Zones.classHeader
            case Zones.funHeader: return Zones.funHeader
            case Zones.funBody: return Zones.funHeader
            case Zones.otherHeader: return Zones.otherHeader
            case Zones.otherBody: return Zones.otherHeader
            case _: raise Exception(f"zone '{self}' non-valid value")

    @property
    def htmlStart(self):
        match self:
            case Zones.classHeader: return '<div style="background-color: #e1f8e1;">'
            case Zones.classBody: return '<div style="border-left: 25px solid #e1f8e1;">'
            case Zones.funHeader: return '<div style="background-color: #fafab4;">'
            case Zones.funBody: return '<div style="border-left: 25px solid #fafab4;">'
            case Zones.otherHeader: return '<div style="background-color: #e9e9f8;">'
            case Zones.otherBody: return '<div style="border-left: 25px solid #e9e9f8;">'
            case Zones.outside: return ''
            case _: raise Exception(f"zone '{self}' non-valid value")
    
    @property
    def htmlEnd(self):
        match self:
            case (Zones.classHeader
                | Zones.classBody
                | Zones.funHeader
                | Zones.funBody
                | Zones.otherHeader
                | Zones.otherBody
                ):
                return '</div>'
            case Zones.outside: return ''
            case _: raise Exception(f"zone '{self}' non-valid value")


def reformat(string_format):
    string_format = string_format.replace('<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%;"><span></span>', '')
    string_format = string_format.replace('</pre></div>\n', '')
    return string_format

def _iter_to_string(iter):
    s = ""
    for i in iter:
        s += i[1]
    return s

def parseFromToken(tokens, formatter, *_, functions_always_in_class=False):
    htmlResult = ""
    depth = [Zones.outside]
    memory = []
    actualIter = []

    def _add_and_clear():
        nonlocal htmlResult, depth, memory, actualIter
        htmlResult += htmlFromIter(actualIter, depth, formatter)
        memory.clear()
        actualIter.clear()

    def nextBlock(beforeZone):
        nonlocal depth
        if functions_always_in_class:
            if (beforeZone is Zones.funHeader and
                Zones.classBody not in depth):
                print("WARNING : The given code seems incomplete, "
                      + "a class indentation has been added to the isolated functions.")
                depth.append(Zones.classBody)
        
        if (beforeZone is Zones.classHeader and
            Zones.classBody in depth):
            print("WARNING: there is a class inside a another class")
        if (beforeZone is Zones.classHeader and
            Zones.funBody in depth):
            print("WARNING: there is a class inside a function")
        if (beforeZone is Zones.funHeader and
            Zones.funBody in depth):
            print("WARNING: there is a function inside a another function")
        
        depth[-1] = depth[-1].logicalFollower
        depth.append(beforeZone)
        _add_and_clear()
        
    def nextBlockSamePlace(newZone):
        nonlocal depth
        depth[-1] = newZone
        _add_and_clear()
    
    def finishBlock(makeZone):
        nonlocal depth
        if not len(depth) > 1:
            raise Exception('unfinished group')
        depth[-1] = makeZone
        _add_and_clear()
        depth.pop()

    for tokenType, tokenValue in tokens:
        actualIter.append((tokenType, tokenValue))

        #Remember
        if tokenValue in java_memory_all_keywords:
            memory.append(tokenValue)
        
        #new block identifier
        if tokenValue == "\n":
            if len(actualIter) == 1:
                #this line is empty
                nextBlockSamePlace(depth[-1].logicalFollower)
            elif all((actualIterTokenType is Token.Comment.Single or actualIterTokenType is Token.Text.Whitespace for (actualIterTokenType, _) in actualIter)):
                #this line has only comments
                nextBlockSamePlace(depth[-1].logicalFollower)
            elif ';' in memory:
                nextBlockSamePlace(depth[-1].logicalFollower)
            elif '{' in memory:
                if (java_memory_conditions | java_memory_loops) & set(memory):
                    nextBlock(Zones.otherHeader)
                elif java_memory_protection & set(memory):
                    if 'class' in memory:
                        nextBlock(Zones.classHeader)
                    else:
                        nextBlock(Zones.funHeader)
                else:
                    raise Exception("Unknown block {")
            elif '}' in memory:
                finishBlock(depth[-1].logicalPreceding)
    
    htmlResult = '<pre>' + htmlResult + '</pre>'
    return htmlResult


def htmlFromIter(iter, depth, formatter):
    formatted_html = ""
    
    for zone in depth:
        formatted_html += zone.htmlStart

    formatted_html += reformat(format(iter, formatter))

    for zone in reversed(depth):
        formatted_html += zone.htmlEnd
    
    return formatted_html

def add_filters(lexer):
    lexer.add_filter(SpecialKeywordFilter())
    return lexer

def format_code(code, *_, functions_always_in_class=False):
    lexer = JavaLexer()
    lexer = add_filters(lexer)
    formatter = HtmlFormatter(noclasses=True, style=BlueJStyle)
    tokens = list(lexer.get_tokens(code))
    return parseFromToken(tokens, formatter, functions_always_in_class=functions_always_in_class)

def create_lines(nbr):
    html = '<td style="padding:0; vertical-align:top; text-align:right; background-color:#bfbfbf; position: sticky; left: 0; width: 1%; white-space: nowrap;"><div><pre>'
    for n in range(1, nbr + 1):
        html += f'<span style="padding-right: 5px; padding-left: 5px;">{n}</span>'
        if n != nbr:
            html += "\n"
    html += "</pre></div></td>"
    return html

def add_container(html_code, border_radius=15):
    html = f'<div style="border-radius:{border_radius}px; overflow-x: auto;"><table style="width: 100%; border-collapse: collapse;"><tbody><tr>'
    html += create_lines(html_code.count("\n"))
    html += '<td style="padding:0; vertical-align:top; text-align:left; background-color:#ffffff;"><div>'
    html += html_code
    html += "</div></td></tr></tbody></table></div>"
    return html

def add_credits(html):
    html += '<pre><i>formatted thanks to <a href="https://github.com/DArtagnant/blueJ-code-highlighter">DArtagnant\'s blueJ-code-highlighter</a><i></pre>'
    return html

def remove_space(code):
    return re_sub(r"^[^\S\r\n]+", "", code, flags=re_m_flag)

def from_file(input_path, output_path, *_, credits=False, border_radius=15, functions_always_in_class=True):
    code = ""
    with open(input_path, "r") as file:
        code = file.read()
    code = remove_space(code)
    result_html = add_container(
        format_code(
            code,
            functions_always_in_class= functions_always_in_class,
            ),
        border_radius=border_radius
        )
    if credits:
        result_html = add_credits(result_html)
    else:
        print("PLEASE ADD THE FORMATTER SOURCE AND AUTHOR'S NAME")
    print("Export terminé")
    with open(output_path, 'w') as file:
        file.write(result_html)

if __name__ == "__main__":
    from_file("input.txt", "output.html")
