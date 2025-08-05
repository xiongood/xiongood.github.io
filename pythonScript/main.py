import requests
from lxml import etree
import re
from pathlib import Path

# 获取第一页 图片地址
srcs = []
url = r'https://www.4kdesk.com/4Kmeinv/index_2.html'
response = requests.get(url)
# print(response.status_code)
# 检查请求是否成功
if response.status_code == 200:
    response.encoding = 'GBK'
    content = response.text
    # print(content)
    tree = etree.HTML(content)
    srcs = tree.xpath("//img[contains(@class, 'lazy')]/@data-original")

# 修改配置文件------------------------------------------------------------------------------------------------------------
# 读取本地hexo的_config.yml文件
# 修改featureImages: 集合的值

# 本地的_config.yml文件
path = Path(r"D:\project\gitee\snb2025\snbBook\themes\hexo-theme-matery-master\_config.yml")


# 读取文件内容
with path.open('r', encoding='utf-8') as f:
    content = f.read()

# 构建新的featureImages内容
images_yaml = "featureImages:\n"
for url in srcs:
    images_yaml += f"- {url}\n"

# 使用正则表达式找到并替换featureImages部分
pattern = r'^featureImages:\s*$(?:\s*-[^\n]*$)*'
updated_content, count = re.subn(
    pattern,
    images_yaml.rstrip(),
    content,
    flags=re.MULTILINE
)

if count == 0:
    # 如果未找到featureImages，则追加到文件末尾
    updated_content = content.rstrip() + "\n\n" + images_yaml.rstrip()

# 写回文件
with path.open('w', encoding='utf-8') as f:
    f.write(updated_content)

