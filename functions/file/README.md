## python2处理中文的相关问题总结

### python2读取文件名含有中文的文件的方法

需要将filename（默认为utf8编码的str类型）解码为unicode才可以，或者直接使用unicode保存含有中文的文件名。

```python
# -*- coding: utf-8 -*-
filename = "demo-中文-20201209v1(1) - 副本.csv".decode("utf-8")
with open(filename, 'r') as fp:
    content_list = fp.readlines()
```

or

```python
# -*- coding: utf-8 -*-
filename = u"demo-中文-20201209v1(1) - 副本.csv"
with open(filename, 'r') as fp:
    content_list = fp.readlines()
```

> 但在python3中没有这个问题。

### 关于控制台Console默认编码

- 在中文版Windows系统中，通常控制台使用gbk编码，因此默认字符串为gbk编码
- 在控制台交互式使用python时，默认编码也为gbk编码
- 在控制台中执行python脚本时，控制台的gbk编码不会影响python脚本（脚本使用utf-8编码）中的编码，但python的print语句需要编码为gbk才可以

```python
# -*- coding: utf-8 -*-
filename = u"demo-中文-20201209v1(1) - 副本.csv"
with open(filename, 'r') as fp:
    content = fp.readline()
print(content.encode('gbk'))
```

### 关于open函数

无论是python2还是python3都需要事先知道文件的编码

- 在python2中，open函数默认编码`以与控制台终端（系统）一致的编码` (**_尚未确认_**) 打开，readline()返回与控制台终端（系统）一致编码的str类型（在python3看来，相当于byte类型）文本

- 在python3中，open函数默认编码与控制台终端（系统）一致，但也可以指定以某编码打开

> 经测试，在gbk编码的控制台中使用python2.7.18测试打开utf-8和gbk编码的文件，readline()都能返回与控制台终端（系统）一致编码的str类型

open函数的替代者：

- codecs.open

```python
# -*- coding: utf-8 -*-
import codecs

filename = u"demo-中文-20201209v1(1) - 副本.csv"
with codecs.open(filename, 'r', encoding='gbk') as fp:
    content = fp.readline()
print(content.encode('utf-8'))
```

- io.open

```python
# -*- coding: utf-8 -*-
import io

filename = u"demo-中文-20201209v1(1) - 副本.csv"
with io.open(filename, 'r', encoding='gbk') as fp:
    content = fp.readline()
print(content.encode('utf-8'))
```