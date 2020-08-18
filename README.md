LinuxBashShellScriptForOps
================
Linux Bash Shell Scripts For Ops, some python scripts here also.

## 这是一个怎样的项目
此项目是对在Linux运维工作所能用到的Shell脚本和Python脚本的归纳和总结。
大部分源码均出自生产系统并经过比较严谨的测试，少部分脚本是用于学习或者测试目的。

遵循**实用**并尽可能的pythonic的原则。

## 为什么有Python的加入
不得不说Python是优秀的编程、脚本语言，用在运维上确实很方便，因为丰富的模块和生态的强大，只需少量时间就可以编写出有用的脚本。

Python不仅是一门高级的跨平台编程语言，而且能轻松实现很多Bash无法实现的功能。

作为运维人员不必排斥编程，编程是为了更好的运维。

## 这个项目里有什么
此项目包含了常用的Shell脚本和Python脚本，主要拆分成两部分：functions和projects。

functions目录存放常用的、基本的脚本语句，用于编写一个完成某项具体事务的脚本。

projects目录存放比较完整的脚本文件，用于做成某件完整的事情。

一些有用的笔记会存放在note.md文件中，也会穿插在代码注释中。

## 关于本项目使用的开发环境和运维环境
本项目通常使用Microsoft Windows 10 中文简体系统进行代码编写，
因此经常会在Python2.x的脚本中发现部分用gbk编解码，特别是用于Windows系统的Python脚本

主要运维环境是CentOS6.x、7.x，Ubuntu16、18 LTS，以及少量的Debian（多用于Docker容器场景）

>因此requirements.txt文件的内容仅用于参考，不作为环境要求

推荐使用JetBrains的PyCharm作为Bash Script和Python的开发工具，并安装配套的Git等工具。

## 如何使用该项目
使用Git工具克隆到本地。

```shell script
git clone https://github.com/DingGuodong/LinuxBashShellScriptForOps.git
```

此项目目前有2个分支用于区分Python2.x和Python3.x，master分支为Python2.x的代码，python3分支为Python3.x的代码。

- [Python2.x 版本](https://github.com/DingGuodong/LinuxBashShellScriptForOps/tree/master)

- [Python3.x 版本](https://github.com/DingGuodong/LinuxBashShellScriptForOps/tree/python3)

在日后的使用过程中不断更新完善和优化。

如果是要使用functions，则需要自己翻阅functions下的所有目录以及各个文件，
或者使用“Find in Path”或者“search in this repository”功能按照关键字搜索。

如果是要使用projects，则可以根据项目的名字查看自己感兴趣或者需要的部分，
或者使用“Find in Path”或者“search in this repository”功能按照关键字搜索。

## 此项目是如何进行和维护的
此项目的所有内容均来自日常的运维工作，因此全部与运维相关，遇到用脚本解决的问题就会写进此项目。

这个项目会持续完善，积累更多有用的Shell、Python编程和运维的相关知识和文件。

此项目完全开源，允许自由复制和使用代码。

欢迎fork和递交pull request。

## 提交bugs和feature requests以及联系信息
可以使用 https://github.com/DingGuodong/LinuxBashShellScriptForOps/issues 页面进行issue提交。

也可以通过issue列出你想通过脚本实现的功能（help wanted，question，feature）、改进建议（enhancement，idea）等。（**推荐）

早些时间，我在51CTO博客中写了大量的关于运维类的原创文章和总结，部分有用的经验也会持续收入本项目。

blog: http://dgd2010.blog.51cto.com

Email: uberurey_ups#163.com

也可加入QQ群与其他人一起交流：

1. QQ群名称：[Bash/Awk/Sed CU论坛](https://jq.qq.com/?_wv=1027&k=5NNyJum) / 群号码：302706076

2. QQ群名称：[运维架构技术交流](https://jq.qq.com/?_wv=1027&k=52fjL0z) / 群号码：991904631

>加入群时请填写有效申请信息，并遵守合理的规则

*欢迎提供其他QQ群，供交流参考，经营性或商业目的除外*

## 编程风格与编程规范 - Programing Style Guides

每个人都可以有自己的编程风格，但使用良好的编程规范可以帮助我们规范代码，也符合大多数人的阅读和使用习惯。

通常一些知名的大厂和团队都会有自己的编程规范，感谢分享！

NO1.从现有的产品或线上中学习，如参考系统中的脚本是如何写的，其他著名项目中的代码是怎样的。

1.[Shell风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-shell-styleguide/contents/) - 中文

2.[Python 风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/contents/) - 中文

3.[Style guides for Google-originated open-source projects](https://github.com/google/styleguide)

4.[PEP 8](https://www.python.org/dev/peps/pep-0008/)

5.[Python best practices guidebook, written for humans.](https://docs.python-guide.org)

6.[Code Review Guidelines](https://docs.gitlab.com/ee/development/code_review.html#everyone)

7.[Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)

当然还有更多优秀的指南或参考，不一一例举。

**最后，记住，规则有时就是用来打破的，做自己当然也是被允许的。**

## TODO List

1. 应该把文档的编写和完善作为一项长期任务，维护好，并保持可用

2. 整理和归纳代码体现的思想和方法，甚至可以让它们脱离代码，独立存在

3. ...
