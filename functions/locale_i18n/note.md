## how to use encoding in Python when reading or writing a file

> how to use encoding in Python when reading or writing a file?

> a `file` can be `.py`(such as in command line), `.csv`, `.html`,`.sql`(query for a database), etc

[Unicode In Python, Completely Demystified （揭秘Python Unicode）](http://farmdev.com/talks/unicode/)

简要罗列一下最重要最实用的点：

Solution

- Decode early （尽早decode, 将"文件"中的内容转化成 unicode 再进行下一步处理)
  > 从文件中读出内容后，立刻解码
- Unicode everywhere (程序内部处理都用unicode)
  >
- Encode late (最后encode回所需的encoding, 例如把最终结果写进结果"文件")
  > 写入文件前才将内容编码

> see also [PYTHON处理中文的时候的一些小技巧](https://coolshell.cn/articles/461.html)

## Why use Unicode in Python?

- handle non-English languages
- use 3rd party modules
- accept arbitrary text input
