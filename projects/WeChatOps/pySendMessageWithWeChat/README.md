##企业名称
    - 运维开发最佳实践
    - OpsDevBestPractice
##企业介绍
    - Linux、Python运维开发最佳实践。为Linux运维人员创建的一个关于Linux、Python的编程、运维最佳实践的公众号，编程是为了更好的运维！
##CorpID
    - wx4dd961cd206edb07
##Secret
    - UZ4e4jCFHySnH6i3X8Ayr-aHvoUhAFhH6yrMI6qnmtGZnIWrEIM7PTEHPvaf30zD
##发消息限制
    - http://qydev.weixin.qq.com/wiki/index.php?title=%E5%8F%91%E6%B6%88%E6%81%AF
    - 企业可以主动发消息给成员，每天可发的数量为：帐号上限数*30人次/天。即200*30=600人次/天。
## 使用方法
    1.在odbp_database.py和odbp_getToken.py.中正确设置“weixin_qy_CorpID”和“weixin_qy_Secret”，分别对应微信企业号ID和对应的密码
    
    2.运行odbp_getToken_usage_example.py查看是否能获得微信Token
    
    3.运行odbp_sendMessage_usage_example.py查看是否能在微信上收到信息
    
    4.运行odbp_sendMessageWithCount_usage_example.py查看能否在微信上收到信息并显示当前使用的信息发送数量
    
    5.从中获得灵感，自己动手开发自己的微信发送消息的Class