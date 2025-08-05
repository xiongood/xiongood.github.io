import os

modified_files = 0
total_files = 0
directory = './public'

def replace_entities_in_file(file_path):
    """替换单个文件中的实体"""
    try:
        print(file_path)
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 替换实体
        new_content = content.replace('&#123;', '{').replace('&#125;', '}')

        # 如果内容有变化才写入
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            return True
        return False

    except UnicodeDecodeError:
        print(f"警告: 无法以UTF-8编码读取文件 {file_path}，已跳过")
        return False
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return False



# 递归遍历目录
for root, dirs, files in os.walk(directory):
    for file in files:
        # 检查是否是HTML文件
        if file.lower().endswith('.html'):
            total_files += 1
            file_path = os.path.join(root, file)
            if replace_entities_in_file(file_path):
                modified_files += 1
                print(f"已修改: {file_path}")









