from pygments import highlight
from pygments.lexers.jvm import JavaLexer
from pygments.formatters import HtmlFormatter

from blueJ_style import BlueJStyle
from create_blocks import addBlocks

code = """public class Main {
  int x = 5;
  /*test
  *a
  */
  public static void main(String[] args) {
    Main myObj = new Main();//commentaire
    System.out.println(myObj.x);
  }
}
"""
lexer = JavaLexer()
formatter = HtmlFormatter(linenos= True,
                          noclasses= True,
                          style= BlueJStyle
                          )
result = highlight(code, lexer, formatter)

result = addBlocks(result)

with open("output.html", 'w') as file:
    file.write(result)