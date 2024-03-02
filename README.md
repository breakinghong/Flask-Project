# Flask-Project-Combat
> There is still a long way to go in the future. I think that as long as I keep exploring, innovation will not be just empty talk, I will go on step by step. You will find that our willpower is sometimes very good, and sometimes it is really bad, but we must continue to do what we decide to do and do well. Sometimes everyone just needs to record the process of their own growth, and when we are old, we can have a good aftertaste, we are all simple people, a long road, step by step.

> Fortunately: We know what path we want to go next. Let us keep moving forward on the road of development.

flask项目实战 keep moving

### 使用flask-sqlalchemy实现数据库的orm

#### 数据库配置
- 常规配置：熟悉不同数据库如何配置
- 更多配置 

| 配置名称                  | 配置意义                                                     |
| ------------------------- | ------------------------------------------------------------ |
| SQLALCHEMY_DATABASE_URI   | 连接数据库的URI配置         |
| SQLALCHEMY_BINDS          | 一个字典，该字典通过绑定的key连接URI                         |
| SQLALCHEMY_ECHO           | 主要用于debug，为True的时候会回显数据库操作的原语            |
| SQLALCHEMY_RECORD_QUERIES | 用于禁用或者启用查询记录。查询记录在调试或者测试模式会自动启用。 |
| SQLALCHEMY_NATIVE_UNICODE | 用于禁用原生的unicode支持。                                  |
| SQLALCHEMY_POOL_SIZE      | 数据库连接池的大小，默认为5                                  |
| SQLALCHEMY_POOL_TIMEOUT   | 指定数据库连接池的连接超时时间                               |
| SQLALCHEMY_POOL_RECYCLE   | 指定多久以后自动回收数据库                                   |

#### sqlalchemy常用字段，选项
- sqlalchemy要对数据库进行映射，也需要对数据库的数据类型进行映射。映射后，sqlalchemy的主要字段类型可以参考下表。

| **字段类型名** | **对应的Python类型** | **字段说明**                                          |
| -------------- | -------------------- | ----------------------------------------------------- |
| Integer        | int                  | 普通整数，一般是 32 位                                |
| SmallInteger   | int                  | 取值范围小的整数，一般是 16 位                        |
| Big Integer    | int 或 long          | 不限制精度的整数                                      |
| Float          | float                | 浮点数                                                |
| Numeric        | decimal.Decimal      | 定点数                                                |
| String         | str                  | 变长字符串                                            |
| Text           | str                  | 变长字符串，对较长或不限长度的字符串做了优化          |
| Unicode        | unicode              | 变长 Unicode 字符串                                   |
| Unicode Text   | unicode              | 变长 Unicode 字符串，对较长或不限长度的字符串做了优化 |
| Boolean        | bool                 | 布尔值                                                |
| Date           | datetime.date        | 日期                                                  |
| Time           | datetime.time        | 时间                                                  |
| DateTime       | datetime.datetime    | 日期和时间                                            |
| Interval       | datetime.timedelta   | 时间间隔                                              |
| Enum           | str                  | 一组字符串                                            |
| PickleType     | 任何 Python 对象     | 自动使用 Pickle 序列化                                |
| LargeBinary    | str                  | 二进制文件                                            |

- 对于不同的字段，可能还会有一些选项，比如该字段是否是主键，该字段的值是否允许重复，这些选项也被称为列选项。sqlalchemy的常见列选项见下表。

| **选项名称** | **选项说明**                                                 |
| ------------ | ------------------------------------------------------------ |
| primary_key  | 如果设为 True，该列就是表的主键，注意：每个模型都应该有一个主键。一般会专门用一个名为id的字段来定义主键 |
| unique       | 如果设为 True，该列不允许出现重复的值                        |
| index        | 如果设为 True，为该列创建索引，提升查询效率                  |
| nullable     | 如果设为 True，该列允许使用空值；如果设为 False，这列不允许使用空值 |
| default      | 为该列定义默认值                                             |

#### 创建模型类

- 导入SQLAlchemy
- 确认数据库配置完整
- 实例数据库链接对象
- 以db.Model为父类，构建数据库模型类
- 数据模型中的字段均是db.Colum类的实例，实例化传参的时候指定字段类型和选项
- 可以重载`__repr__`魔法方法，让模型对象有更好的可读性，不是必须实现的

### 数据库迁移

#### 创建迁移仓库 init
```python
python manager.py db init
```
**需要注意，模型类是否能够在迁移过程中执行到，需要导包暴露出来**
#### 创建迁移脚本
- 自动创建迁移脚本有两个函数
  - upgrade()：函数把迁移中的改动应用到数据库中。
  - downgrade()：函数则将改动删除。

- 自动创建的迁移脚本会根据模型定义和数据库当前状态的差异，生成upgrade()和downgrade()函数的内容。

- 对比不一定完全正确，有可能会遗漏一些细节，需要进行检查

```python
python manager.py db migrate -m 'initial migration'
# 运行命令之后。可以看到migration文件夹中新增了数据库迁移的版本文件并没有在数据库也只是创建了版本号，并没有生成对应的表。
```
#### 更新数据库
```shell
python manager.py db upgrade
```

> 迁移操作步骤
```
实际操作顺序:
1.python 文件 db init
2.python 文件 db migrate -m"版本名(注释)"
3.python 文件 db upgrade 然后观察表结构
4.根据需求修改模型
5.python 文件 db migrate -m"新版本名(注释)"
6.python 文件 db upgrade 然后观察表结构
7.若返回版本,则利用 python 文件 db history查看版本号
8.python 文件 db downgrade(upgrade) 版本号
```

## 配置文件加载
### 直接配置
```python
app.config['HOST']="访问域名"
```
### 通过对象加载 from_object()
```python
app.config.from_object(ProductionConfig)
```
### 通过环境变量加载
#### from_envvar方法实现
```shell
HOST=localhost
export CONFIG_SET=./config.py
```
代码中使用from_envvar加载，底层使用的是from_pyfile
```python
app.config.from_envvar('CONFIG_SET')
```
#### python-dotenv加载
```python
# `.env`
MAIL_PORT = 465
MAIL_USE_SSL = false
MAIL_USE_TLS = true
```
```python
# settings.py
class BaseConfig(object):
    ...
    MAIL_PORT = int(os.getenv('MAIL_PORT', default=587))
    MAIL_USE_SSL = True if 'true' == os.getenv('MAIL_USE_SSL') else False
    MAIL_USE_TLS = True if 'true' == os.getenv('MAIL_USE_TLS') else False
```
```python
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)  #  override=True: 覆写已存在的变量

```
### 加载配置文件
#### py文件
```python 
vim confile.py
HOST='locolhost'
...
app.config.from_pyfile('./confile.py') #加载配置文件
```
#### conf文件
```ini
vim test.conf
[api] # section
port=8000 # option
```
```python
import configparser


def getconfig(filename, section=''):
    cf = configparser.ConfigParser()  # 实例化
    cf.read(filename)  # 读取配置文件
    cf_items = dict(cf.items(section)) if cf.has_section(
        section) else {}  # 判断SECTION是否存在,存在把数据存入字典,没有返回空字典
    return cf_items
```

#### ini文件
- 类似conf操作方式通过ConfigParser解析出相应的配置字典进行加载

#### yaml文件
- 什么是yaml文件？
- YAML是一种直观的能够被电脑识别的的数据序列化格式，容易被人类阅读，并且容易和脚本语言交互。YAML类似于XML，JSON等，但是语法简单得多，对于转化成数组或可以hash的数据时是很简单有效的。

```yaml
# yaml格式
name: 张三
age: 37
children:
 - name: 小明
   age: 15
 - name: 小红
   age: 12
```

```python
{
'name': '张三', 'age': 37, 
'children': [{'name': '小明', 'age': 15}, {'name': '小红', 'age': 12}]
}
```
```yaml
COMMON: &common
  SECRET_KEY: insecure
  DEBUG: False
  
DEVELOPMENT: &development
  <<: *common
  DEBUG: True
  
STAGING: &staging
  <<: *common
  SECRET_KEY: sortasecure

PRODUCTION: &production
  <<: *common
  SECRET_KEY: mdd1##$$%^!DSA#FDSF
```

```python
import yaml
def read_yaml(yaml_file_path):
    with open(yaml_file_path, 'rb') as f:
        cf= f.read()
    cf = yaml.load(cf)
return cf
```
```python
from flask import Flask
app = Flask(__name__)
cf = read_yaml("setting.yaml")
app.config.update(cf)
```
```python
from flask import Flask
import yaml
def read_yaml(yaml_file_path):
    with open(yaml_file_path, 'rb') as f:
        cf= yaml.safe_load(f.read()) # yaml.load(f.read())
return cf

app = Flask(__name__)
cf = read_yaml("setting.yaml")
app.config.update(cf)

if __name__ == "__main__":
    app.run()
```
#### json文件
```python
import os
import json
from flask import Flask


def create_app():
    app = Flask('test')
    # 这里在虚拟环境中设置环境变量。 export RMON_CONFIG=xxx.json
    file = os.environ.get('RMON_CONFIG')
    content = ''
    if file:
        rest = {}
        with open(file) as f:
            for line in f:
                #  if line.strip().startswith('#'):
                if "#" in line:
                    continue
                content += line
    if content:
        config = json.loads(content)
        for k in config:
            app.config[k.upper()] = config[k]
    return app


if __name__ == '__main__':
    create_app()
```