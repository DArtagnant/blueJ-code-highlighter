import re

#/\*(?!_BJCH)[\s\S]*?\*/\n(?:\b(?:public|private)\b.*\bclass\b)[\s\S]*?^(?<!\s{2})\}
#\n?(?:\b(?:public|private)\b.*\bclass\b)[\s\S]*?^(?<!\s{2})\}
#/\*(?!_BJCH)[\s\S]*?\*/\n(?:\b(?:public|private)\b.*\bclass\b).*?$
REGEX_FIND_CLASS = re.compile(r"\n?(?:\b(?:public|private)\b.*\bclass\b)[\s\S]*?^(?<!\s{2})\}", re.MULTILINE)
REGEX_FIND_FUNCTION = re.compile(r"\n?(?:\b(?:public|private)\b(?!.*\bclass\b))[\s\S]*?^\s{2}\}", re.MULTILINE)
REGEX_FIND_SPACE = re.compile(r"^  |(?<=>)  ", re.MULTILINE)

CLASS_KEYWORD_START = "_BJCH_startClass"
CLASS_KEYWORD_END = "_BJCH_endClass"
FUN_KEYWORD_START = "_BJCH_startFun"
FUN_KEYWORD_END = "_BJCH_endFun"
SPACE_KEYWORD = "_BJCH_Space"

def regex_find_span(keyword):
    return re.compile(r"\n<span[^>]*?>/\*" + keyword + r"\*/</span>\n\n?")


#Does not work with unindented code and with function in functions

def add_format(format, index, formatted_code, plus_index):
    formatted_code = formatted_code[:index+plus_index] + "\n/*" + format + "*/\n" + formatted_code[index+plus_index:]
    plus_index += len(format) + 6
    return formatted_code, plus_index

def detectBlocks(code):
    formatted_code = code
    plus_index = 0
    
    for r_match in REGEX_FIND_CLASS.finditer(code):
        formatted_code, plus_index = add_format(CLASS_KEYWORD_START, r_match.start(), formatted_code, plus_index)
        formatted_code, plus_index = add_format(CLASS_KEYWORD_END, r_match.end(), formatted_code, plus_index)
    plus_index = 0
    for r_match in REGEX_FIND_FUNCTION.finditer(formatted_code):
        formatted_code, plus_index = add_format(FUN_KEYWORD_START, r_match.start(), formatted_code, plus_index)
        formatted_code, plus_index = add_format(FUN_KEYWORD_END, r_match.end(), formatted_code, plus_index)
    
    #formatted_code = REGEX_FIND_SPACE.sub(f"/*{SPACE_KEYWORD}*/", formatted_code)
    return formatted_code




def addBlocks(code, remove_space):
    #<pre style="background-color: #d6bd00">
    #<span[^>]*>public<\/span>
    code = regex_find_span(CLASS_KEYWORD_START).sub('<div style="background-color: #e1f8e1">', code)
    code = regex_find_span(CLASS_KEYWORD_END).sub('</div>\n', code)

    code = regex_find_span(FUN_KEYWORD_START).sub('<div style="background-color: #fafab4">  ', code)
    code = regex_find_span(FUN_KEYWORD_END).sub('</div>', code)
    code = REGEX_FIND_SPACE.sub('<span style="background-color: #e1f8e1">  </span>', code)
    if remove_space:
        code = re.sub("line-height: 125%;", "line-height: 100%;", code)
    return code