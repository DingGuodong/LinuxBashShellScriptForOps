## How To Learn Bash and Python Programming The Smart Way

## 如何聪明地学习Bash和Python编程

>说明：
>
>本文是从运维的角度总结和撰写，主要是想让后来者少走弯路、节约时间，
>而且更重要恰好就是运维不仅要懂运维，一定要懂点开发。
>阅读本文可能需要一些运维开发基础，且假定读者已经拥有一些编程基础。
>本文不是一个大而全的指导手册，也不是细致入微的分析教程，
>仅用于总结一些学习的思路和方法，或作为一个跳板，引导读者进入一些更高级的内容（这些可以在网上或者参考手册中找到）。

### 一般性方法

1. 记住学习它的目的和动机，且最好把它写下来

2. 了解自己，相信自己、用心去做并保持耐心

3. 了解它能做什么不能做什么，擅长什么不擅长什么，什么时候用它什么时候用其他

4. 先本着应用的目的去学习，刚开始不要钻细节，先知道How再去了解Why

5. 选择适合自己的学习材料和学习方式，适合自己的才是最佳的

6. 借鉴他人的经验，借鉴他人使用的学习材料、作品

7. 知道如何提问问题和寻找问题的答案

8. 学会自己思考，不要只局限于编程语言本身

9. 保持良好的学习和使用状态，经常使用，教或帮助别人，形成良性循环

10. 做好人，做正确的事，坚守底线，不作恶


### 如何学习Bash

通常学习Bash编程是为了满足工作的需要，也可能是兴趣使然。

Bash通常是绝大部分GNU/Linux的默认shell，通过Bash脚本可以实现Linux下大部分的日常运维管理工作，
包括系统配置、服务管理、计划任务、文件管理、数据处理等几乎全部操作。

Bash的优势是用户平时就直接使用它，这使得用户非常平滑的接受bash编程，学习成本比较低。
另外编写起来非常高效，简短的命令组合和管道（“|”）就可实现非常复杂的功能。

缺点是大型项目或者复杂的操作不便于管理维护，严重依赖bash周边工具才能实现复杂的功能，如Web管理、接口调用等。

##### Bash参考资料
bash编程的学习资料一般需参考官方手册，可以通过man命令或者网页浏览即可。

1. man bash

2. [Bash参考手册](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html)

3. [Linux文档项目, LDP](http://www.tldp.org/)

4. [Advanced Bash-Scripting Guide, ABS](http://www.tldp.org/LDP/abs/html/index.html)

5. [Bash Guide for Beginners](http://www.tldp.org/LDP/Bash-Beginners-Guide/html/index.html)

##### Bash编程推荐书籍和扩展阅读

>_Tips：以下书名大部分可以通过搜索引擎搜索到，也可以直接打开[豆瓣读书](https://book.douban.com/)进行搜索。_

1. 《UNIX环境高级编程（第3版）》 人民邮电出版社 W.Richard Stevens

2. 《Linux命令行与shell脚本编程大全 人民邮电出版社 Richard Blum

3. 《跟老男孩学Linux运维：Shell编程实战》机械工业出版社 老男孩

4. 《Linux命令、编辑器与shell编程（第三版）》 清华大学出版社 Sobell·M.G

5. 《Linux、Unix设计思想》人民邮电出版社 甘卡兹

6. 《UNIX编程艺术》 电子工业出版社 雷蒙德  注：了解一下Unix哲学

### 如何学习Python

python是一门简单、易用、能干的语言。

python跨平台已经非常友好了，这种解释性语言除了比不上shell的原生性和自身生态，其他都超过了。

Python几乎是一门万能的语言，有非常多的库，
可用于系统管理、Web服务、系统或应用软件、数据分析，除此之外Python还是云厂商经常提供的SDK的语言之一。

>_Tips：建议将Python3.x作为入门首选版本。_

##### Python编程推荐书籍和参考链接

1. [Python - 100天从新手到大师](https://github.com/jackfrued/Python-100-Days)

2. [Python 3 标准库实例教程](https://learnku.com/docs/pymotw)

3. [Python Cookbook 3rd Edition](https://python3-cookbook.readthedocs.io/zh_CN/latest/index.html)

4. 《Python自动化运维 技术与最佳实践》机械工业出版社 刘天斯

5. 《Python编程：从入门到实践》 人民邮电出版社 埃里克·马瑟斯（Eric Matthes）

6. 《流畅的Python》 人民邮电出版社 Luciano Ramalho

7. 《编写可读代码的艺术》 机械工业出版社 鲍斯威尔（Boswell,D.）

8. 《Python编程快速上手 让繁琐工作自动化》 人民邮电出版社 Al Sweigart

9. 《Effective Python:编写高质量Python代码的59个有效方法》

10. 《Python高级编程》 人民邮电出版社 Tarek Ziadé

##### Python开源项目

1. [httpbin](https://github.com/postmanlabs/httpbin)

    >注：之所以单独列出httpbin是因为它可以作为后端服务用于很多种运维和测试场景。
    如SLB、Nginx配置、API及Web Service替代品等。

2. [更多](https://github.com/search?l=Python&o=desc&q=python&s=stars&type=Repositories)

>欢迎通过issue或者PR的方式进行校正、补充
