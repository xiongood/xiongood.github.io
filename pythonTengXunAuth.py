import os

# 定义目录和文件名
directory = "./public"
filename = "c76c82749449274fdad08560b01a1e5f.txt"
content = "1cb44d145c5cbab1c32c321c92aba0f483884ed9"

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
