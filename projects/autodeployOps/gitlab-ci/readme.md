# gitlab ci 配置要求和思路
1. 能区分不同的环境，如test、staging、prod等
2. 能灵活的配置目标主机信息，如ssh的ip、port、user等
3. 能灵活的配置服务（应用）信息，如部署路径，服务端口号，健康检测方法
4. 能准确的判断是否部署成功
5. 可以适当的使用gitlab ci自带的变量用于部署或者信息查看
---

## 部署思路
通常部署脚本可以采用多种语言，可以使用bash script或者python script

bash script的优势是大多Linux系统自带，一般无需安装配置，gitlab ci使用的image在满足基本需要的情况下可以任意选择。

python一般依赖众多模块，需要仔细配置gitlab ci使用的image以至于image可能比较大，
或者需要执行较多的before_script命令行导致pipeline时间较长。

## 部署脚本的编写思路
部署脚本分为两部分：部署操作和服务管理，分别可对应两个脚本

部署操作脚本的功能：执行部署操作，调用服务管理脚本；
执行服务启动操作，执行服务健康检查操作

初始化配置后，判断当前部署环境，获取当前部署环境中的变量，完成初始化部署配置

读取每一个部署服务器的信息，有次序的逐个部署，失败则退出，部署成功且服务健康检查通过后则继续部署下一个服务器



## 配置信息的存取
1. 存储到.gitlab-ci.yml中的variables中，key:value形式，每个环境一个配置。
2. 私密信息（如passwords、token、secret keys）存储到<project-url>/settings/ci_cd中的“Secret Variables”中，key:value形式。
>Secret Variables
>
>These variables will be set to environment by the runner.
>So you can use them for passwords, secret keys or whatever you want.
>The value of the variable can be visible in job log if explicitly asked to do so.

>注： 如果在脚本内发现一个变量并没有在脚本中定义，则它要么在.yml中定义要么在“Secret Variables”中定义。

## image的命名规则
image用于build和deploy操作，可能需要很多运行环境，比如python版本、jdk版本等，需要在tag名称中显著表明主要版本。

示例：
```yaml
image: "registry.gitlab.com/gitlab-org/gitlab-build-images:ruby-2.6.3-golang-1.11-git-2.22-chrome-73.0-node-12.x-yarn-1.16-postgresql-9.6-graphicsmagick-1.3.33"
```
