import javalang

def extract_classes(java_code):
    tree = javalang.parse.parse(java_code)
    classes = {}
    for path, node in tree:
        if isinstance(node, javalang.tree.ClassDeclaration):
            start_position = node.position[0][0]
            end_position = node.position[1][0]
            classes[node.name] = java_code[start_position:end_position]
    return classes

java_code = """
public class MyClass {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

class AnotherClass {
    // Some code here
}
"""

classes = extract_classes(java_code)
for class_name, class_code in classes.items():
    print(f"Class: {class_name}\nCode:\n{class_code}\n")
