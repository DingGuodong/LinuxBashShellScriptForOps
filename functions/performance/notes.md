## 关于进程和线程

一般地，任务（作业）分为CPU密集型和IO密集型，什么样的类型决定了应该选择使用什么样的库和方法。

1. CPU密集型(也叫作计算型) --> 需要并行 --> 用多进程 --> 高消耗CPU --> from multiprocessing import Pool

2. IO密集型 --> 需要并发 --> 用多线程 --> 低消耗CPU --> from multiprocessing.pool import ThreadPool

多进程是并发，多线程是并行，如果要尽快完成大批量任务，可以使用多进程多线程（开启多个进程，每个进程开启多个线程）

Tips: 在Python3中可以利用[concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
实现并行计算，使用ProcessPoolExecutor实现多进程（充分地利用每一个CPU核心，但进程数不建议超过CPU核心数量），处理计算密集型任务，
使用ThreadPoolExecutor实现多线程（线程数可以超过CPU核心数量），处理IO密集型任务。

Tips：如何判断CPU密集型还是IO密集型，所有操作是通过CPU和内存内的数据完成的，则这一般是CPU密集型（如计算哈希），
反之，产生IO的操作一般是IO密集型（如下载文件）
