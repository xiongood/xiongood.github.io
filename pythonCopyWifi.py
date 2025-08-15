import shutil
import os

# 源文件路径
source_file = "wifi.html"

# 目标文件夹路径
target_dir = "./public"

# 目标文件路径
target_file = os.path.join(target_dir, "wifi.html")

try:
    # 复制文件
    shutil.copy2(source_file, target_file)
    print(f"文件 '{source_file}' 已成功复制到 '{target_file}'")
except Exception as e:
    print(f"复制文件时发生错误: {str(e)}")
