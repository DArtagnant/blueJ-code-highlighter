import os
from highlight import from_file

def find_jar_files(directory):
    jar_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                jar_files.append(os.path.join(root, file))
    return jar_files

if __name__ == "__main__":
    input_dir = r""
    output_dir = r""
    jar_files_paths = find_jar_files(input_dir)
    for jar_file_path in jar_files_paths:
        print(f"found {jar_file_path} : working")
        from_file(jar_file_path, os.path.join(output_dir, jar_file_path.replace("\\", "_").replace("/", "_")) + ".html")
        print(f"{jar_file_path} ok")
    print("done")