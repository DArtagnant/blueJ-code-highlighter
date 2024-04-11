# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"(?:\b(?:public|private)\b.*\bclass\b)[\s\S]*?^(?<!\s{2})\}"

test_str = ("public class Main {\n"
	"  int x = 5;\n"
	"  /*test\n"
	"  *a\n"
	"  */\n"
	"  public static void main(String[] args) {\n"
	"    Main myObj = new Main();//commentaire\n"
	"    System.out.println(myObj.x);\n"
	"  }\n"
	"  private static void main(String[] args) {\n"
	"    Main myObj = new Main();//commentaire\n"
	"    System.out.println(myObj.x);\n"
	"  }\n"
	"}\n\n"
	"public class Main {\n"
	"  int x = 5;\n"
	"  /*test\n"
	"  *a\n"
	"  */\n"
	"  public static void main(String[] args) {\n"
	"    Main myObj = new Main();//commentaire\n"
	"    System.out.println(myObj.x);\n"
	"  }\n"
	"  private static void main(String[] args) {\n"
	"    Main myObj = new Main();//commentaire\n"
	"    System.out.println(myObj.x);\n"
	"  }\n"
	"}\n")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
