import re

#Does not work with unindented code
RE_CLASS = re.compile(r"^(/\*[\s\S]*?\*/\n)?(\b(?:public|private)\b.*\bclass\b[\s\S]*?$)([\s\S]*?\{$[\s\S]*?(?<!  )\})", re.MULTILINE)
RE_FUN = re.compile(r"(^  /\*[\s\S]*?\*/\n)?(^  (?:public|private)\b[\s\S]*?$)([\s\S]*?^  \})", re.MULTILINE)
RE_SPACE = re.compile(r"^    |^  |(?<=#)  ", re.MULTILINE)


CLASS_START = "#classStart#"
CLASS_END = "#classEnd#"
FUN_START = "#funStart#"
FUN_END = "#funEnd#"

def add_format(format, index, formatted_code, plus_index):
    formatted_code = formatted_code[:index+plus_index] + format + formatted_code[index+plus_index:]
    plus_index += len(format)
    return formatted_code, plus_index

def detectBlocks(code):
    formatted_code = code
    plus_index = 0
    for r_match in RE_CLASS.finditer(code):
        formatted_code, plus_index = add_format(CLASS_START, r_match.start(), formatted_code, plus_index)
        formatted_code, plus_index = add_format(CLASS_END, r_match.end(), formatted_code, plus_index)
    plus_index = 0
    for r_match in RE_FUN.finditer(formatted_code):
        formatted_code, plus_index = add_format(FUN_START, r_match.start(), formatted_code, plus_index)
        formatted_code, plus_index = add_format(FUN_END, r_match.end(), formatted_code, plus_index)
    
    formatted_code = RE_SPACE.sub("", formatted_code)
    return formatted_code


def addBlocks(code, remove_space):
    code = re.sub(CLASS_START, '</span><div style="border-left: 25px solid #e1f8e1;"><span>', code)
    code = re.sub(CLASS_END, '</span></div><span>', code)
    code = re.sub(FUN_START, '</span><div style="border-left: 25px solid #fafab4;"><span>', code)
    code = re.sub(FUN_END, '</span></div><span>', code)
    return code