# Git分布式版本控制系统

为什么说Git是分布式的，原因是Git仓库的每一个参与者都拥有Git仓库的完整副本， 本地修改和提交不依赖于Git服务器，只有参与者之间同步数据时才需要Git服务器。

参考：[Git 使用教程](https://mp.weixin.qq.com/s/4SXOU4cTAjk3HPmpu8IgEw)
> SVN是集中式版本控制系统，版本库是集中放在中央服务器的，而干活的时候，用的都是自己的电脑，所以首先要从中央服务器哪里得到最新的版本，然后干活，干完后，需要把自己做完的活推送到中央服务器。集中式版本控制系统是必须联网才能工作，如果在局域网还可以，带宽够大，速度够快，如果在互联网下，如果网速慢的话，就纳闷了。
>
>Git是分布式版本控制系统，那么它就没有中央服务器的，每个人的电脑就是一个完整的版本库，这样，工作的时候就不需要联网了，因为版本都是在自己的电脑上。既然每个人的电脑都有一个完整的版本库，那多个人如何协作呢？比如说自己在电脑上改了文件A，其他人也在电脑上改了文件A，这时，你们两之间只需把各自的修改推送给对方，就可以互相看到对方的修改了。

## git服务器

推荐使用github和gitlab，其中gitlab可以独立部署（本地化部署）

## git概念和基础知识

仓库又叫版本库，英文名称repository，以目录的形式呈现给Git用户。

Git有两个repository，远程仓库（remote）和本地仓库（local），其中remote并不是必须的

远程库的默认名称是origin，即远程库上的分支通常以origin/xxx/xyz表示，而本地仓库上的分支一般以xxx/xyz表示。

本地仓库涉及两个区，工作区和暂存区，已经add但未commit的文件在暂存区。

1. 使用 git add 把文件添加进去，实际上就是把文件添加到暂存区。
2. 使用git commit提交更改，实际上就是把暂存区的所有内容提交到本地仓库的当前分支上，尚未push到远程仓库。

HEAD是git指向当前分支节点的一个指针，也叫游标。它可以指向分支里的任何一个节点，通常也会把它理解为表示当前的分支。

git fetch 更新的是本地仓库中的origin部分，并不影响本地仓库中已经创建、打开、签出的分支。

git pull 是git fetch + git merge的组合。git pull是把远程仓库更新到本地仓库。
> 注意：pull操作可能会影响工作区，而fetch只影响本地仓库，merge操作并不影响本地仓库，只有commit后才会被提交。
>
>pull后，如果远程仓库和工作区文件存在冲突，则会自动提示，并显示出差异。

追踪（tracking）：本地分支与远程分支之间如果关联，则本地分支是远程分支的跟踪，跟踪某些场景会自动创建，比如同名情况。

## git工作流（workflow/flow）

将仓库区分为公共仓库和个人仓库，公共仓库是发布release的仓库，不作日常开发使用。 项目参与者通过fork公共仓库到个人仓库，所有的日常操作均在个人仓库完成。

公共仓库一般不允许push，只能通过merge进行（提交拉取请求pull requests）。

无论是公共仓库还是个人仓库，master分支一般不允许直接push（可设置为受保护的分支），只能通过由其他分支merge到master。

在这种工作流下，公共仓库一般作为为upstream（这并不是一个git 关键词），而个人仓库实则为remote也就是origin。 upstream允许fetch，而origin允许push。

添加仓库作为upstream，以便于将公共仓库同步到个人仓库，使用如下命令：

```shell script
git remote add upstream git://github.com/public/repo.git
git fetch upstream
git merge upstream/master
git push origin master
```

## 常见问题FAQ

1. 当工作区已经有修改但未提交的文件存在冲突时应该如何解决？

- 保留当前工作区修改

```shell
git stash # 将本地的状态暂时保存起来
git pull origin master
git stash pop # 将暂时保存起来本地的状态还原回来
```

- 不保留当前工作区修改

```shell
git reset --hard  # 将本地的状态恢复到上一个commit id
git pull origin master
```

2. 其他问题

> 规则：在任何时候，在用户使用的任何一个版本都必须在任何时刻在git中找到，他们必须是1对1的关系。

## 运行环境

|简称|全称|
|  :----  | :----  |
|DEV|Development environment|
|FAT|Feature Acceptance Test environment|
|UAT|User Acceptance Test environment|
|PRO|Production environment|

## git分支管理

简单的版本

|分支|名称|说明|
|:----|:----|:----|
|master|主分支|用于发布release，正式环境|
|develop|测试分支|用于开发和修复，测试环境|
|feature|需求开发分支|用于日常开发，测试环境|

复杂一点的版本

参考：[Git 分支设计规范](https://www.cnblogs.com/xinliangcoder/p/12336576.html)

|分支|名称|可发布到的环境|说明|
|:----|:----|:----|:----|
|master|主分支|PRO||
|release|预上线分支|UAT||
|hotfix|紧急修复分支|DEV|发布后删除即可|
|develop|测试分支|FAT||
|feature|需求开发分支|DEV|发布后删除即可|

> 如果包含独立部署、特殊定制或封版的分支，建议放release分支
> 习惯上，release上的版本是可发布可正式使用的版本

## git命令

暂略

## others

### commit规范

1. 提交信息最好能反映出提交修改的意图，简单明了、清晰直观。
2. 字数不要过长，建议不超过60字
3. 可以附加issue编号

### .gitignore

ignore顾名思义是不提交到仓库。 在提交时，可以先确定哪些文件或目录需要ignore。

## GitHub Authentication Tips

应该通过命令行或 API 创建个人访问令牌（Personal Access Token）来代替密码。

在使用GitHub API 或命令行时，可使用个人访问令牌 (PAT) 代替密码向 GitHub 进行身份验证。

### 在命令行上使用令牌（Token）

如果您有令牌，则可以在通过 HTTPS 执行 Git 操作时输入令牌，而不是密码。

例如，在命令行中输入以下内容：

```text
$ git clone https://github.com/username/repo.git
Username: your_username
Password: your_token
```

个人访问令牌只能用于 HTTPS Git 操作。 如果您的仓库使用 SSH 远程
URL，则需要[将远程 URL 从 SSH 切换到 HTTPS](https://docs.github.com/cn/articles/changing-a-remote-s-url/#switching-remote-urls-from-ssh-to-https)。

如果没有提示您输入用户名和密码，说明您的凭据可能已缓存在计算机上。
您可以[在密钥链中更新您的凭据](https://docs.github.com/cn/articles/updating-credentials-from-the-osx-keychain)，用令牌替换您的旧密码。

### Windows删除凭据

进入"仓库根目录/.git"，编辑"config"文件，将`[credential ".*.git"]`节中的`helper = .*`注释或删除，重新push，按照指引配置。
