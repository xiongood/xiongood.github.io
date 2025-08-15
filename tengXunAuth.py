import os

# 定义目录和文件名
directory = "./public"
filename = "c02f16713e69a269186ba5f4acf3a14f.txt"
content = "f11081790563918932379b0deb40e52741d187db"

# 确保目录存在，如果不存在则创建
os.makedirs(directory, exist_ok=True)

# 拼接完整的文件路径
file_path = os.path.join(directory, filename)

try:
    # 写入文件内容
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"文件已成功创建: {file_path}")
except Exception as e:
    print(f"创建文件时出错: {e}")
