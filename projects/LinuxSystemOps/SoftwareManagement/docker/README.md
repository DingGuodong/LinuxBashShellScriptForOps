# About getDockerContainerInfoWithPidNumber.py

### What problem to solve?

Usually, we can NOT find a process comes from which docker container using with 'ps', etc commands on host.

通常我们不能在主机上通过“ps”等命令判断一个docker进程来自哪一个容器。

With this file, you can input a pid number to it, and you will get a useful low-level information on a container from
'docker inspect \<id\>' to
help you find out which container does it come from.

借助这个文件，给它输入一个pid数字，它就能调用 'docker inspect \<id\>'命令打印出详细的信息，
帮助你判断这个进程来自哪一个容器。

### Requirement:

Docker Server Version >= 1.11, you can use 'docker info' to find docker server version out.

要求：
Docker Server Version >= 1.11，可以使用'docker info '判断docker server的版本。
