---
title: python链接mysql数据库
author: 张一雄
summary: 爬取壁纸网站
categories:
 - 后端
tags:
 - python
 - mysql
---



## 下载工具包

```shell
pip install sqlalchemy mysql-connector-python
```
## 写配置
```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 定义ORM基类
Base = declarative_base()


# 定义User模型
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Dog(Base):
    __tablename__ = 'dog'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)

    def __repr__(self):
        return f"<Dog(id={self.id}, name='{self.name}', age='{self.age}')>"


# 创建数据库引擎（这里假设MySQL服务运行在localhost，端口为3306，数据库名为mydatabase）
# 请根据你的实际配置替换以下信息
engine = create_engine('mysql+mysqlconnector://root:Xiong1991@101.200.135.70:3306/py-test')

# 创建DBSession类型
Session = sessionmaker(bind=engine)

# 创建session对象
session = Session()

# 创建表（如果尚不存在）
Base.metadata.create_all(engine)

```
## 测试新增和查询
```python
# 创建一个新用户
from Db import User, session, Dog

new_user = User(id=7, name='Alice', email='alice@example.com')
new_dog = Dog(id=7, name='Alice', age=15)

# 添加到session
session.add(new_user)
session.add(new_dog)
# 查询
users = session.query(User).all()
dogs = session.query(Dog).all()
for user in users:
    print(user)
for dog in dogs:
    print(dog)
# 提交事务到数据库
session.commit()

```
## 测试修改
```python
# 更新用户信息
from Db import session, User

user_to_update = session.get(User, 4)
user_to_update.name = 'Alice Updated'
user_to_update.email = 'alice_updated@example.com'
# 提交事务到数据库
session.commit()

```

## 测试删除
```python
# 删除用户
from Db import session, User

user_to_delete = session.get(User, 4)
session.delete(user_to_delete)
# 提交事务到数据库
session.commit()
```
