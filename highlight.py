from pygments import highlight
from pygments.lexers.jvm import JavaLexer
from pygments.formatters import HtmlFormatter

from blueJ_style import BlueJStyle
from create_blocks import detectBlocks, addBlocks

code =""""""

with open("input.txt", "r") as file:
    code = file.read()

code = detectBlocks(code)

lexer = JavaLexer()
formatter = HtmlFormatter(noclasses= True,
                          style= BlueJStyle,
                          )
result = highlight(code, lexer, formatter)
#print(result)
result = addBlocks(result, remove_space=False)

with open("output.html", 'w') as file:
    file.write(result)