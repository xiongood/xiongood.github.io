# 读取文件内容
with open(r"./node_modules/hexo-prism-plugin/src/index.js", "r", encoding="utf-8") as f:
    content = f.read()

# 定义新的map对象
new_map = """const map = {
  '&#39;': '\'',
  '&amp;': '&',
  '&gt;': '>',
  '&lt;': '<',
  '&quot;': '"',
  '&#123;': '{',
  '&#125;': '}'
};"""

# 查找并替换map部分（从const map = {开始到};结束）
start = content.find("const map = {")
end = content.find("};", start) + 2  # 包含};
modified_content = content[:start] + new_map + content[end:]

# 写回文件
with open(r"./node_modules/hexo-prism-plugin/src/index.js", "w", encoding="utf-8") as f:
    f.write(modified_content)

print("map对象已更新")

