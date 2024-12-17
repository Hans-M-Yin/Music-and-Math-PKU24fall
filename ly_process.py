import os
import re

def process_lilypond_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 处理每一行
    modified_lines = []
    for line in lines:
        # 删除 \RemoveEmptyStaffContext 行
        if '\\RemoveEmptyStaffContext' not in line:
            # 修正 override 属性
            line = re.sub(r"\\override VerticalAxisGroup #'remove-first", r"\\override VerticalAxisGroup.remove-first", line)
            modified_lines.append(line)

    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)

def process_directory(directory):
    # 遍历目录中的所有 .ly 文件
    for filename in os.listdir(directory):
        if filename.endswith('.ly'):
            file_path = os.path.join(directory, filename)
            process_lilypond_file(file_path)
            print(f"Processed: {file_path}")

if __name__ == "__main__":
    # 设置要处理的目录
    directory_path = input("Enter the directory path containing .ly files: ")
    process_directory(directory_path)