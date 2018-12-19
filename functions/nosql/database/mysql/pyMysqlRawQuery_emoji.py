#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyMysqlRawQuery.py
User:               Guodong
Create Date:        2016/12/1
Create Time:        21:06

MySQL RAW SQL query(insert a emoji)

# Character setting in mysql server
----------------------------------------------------------------------------------------------------
mysql> show variables like "%char%";
+--------------------------+---------------------------------------------------------+
| Variable_name            | Value                                                   |
+--------------------------+---------------------------------------------------------+
| character_set_client     | gbk                                                     |
| character_set_connection | gbk                                                     |
| character_set_database   | utf8                                                    |
| character_set_filesystem | binary                                                  |
| character_set_results    | gbk                                                     |
| character_set_server     | utf8                                                    |
| character_set_system     | utf8                                                    |
| character_sets_dir       | C:\Program Files\MySQL\MySQL Server 5.6\share\charsets\ |
+--------------------------+---------------------------------------------------------+
8 rows in set (0.00 sec)

mysql>

# Table structure for emoji
----------------------------------------------------------------------------------------------------
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for emoji
-- ----------------------------
DROP TABLE IF EXISTS `emoji`;
CREATE TABLE `emoji`  (
  `id` int(11) NOT NULL,
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of emoji
-- ----------------------------
INSERT INTO `emoji` VALUES (1, 'test1');
INSERT INTO `emoji` VALUES (2, '😄');

SET FOREIGN_KEY_CHECKS = 1;


 """
import pymysql

emoji_item = u'\U0001f604'.encode('utf-8')  # '😄'
sql = "INSERT INTO `test`.`emoji`(`id`, `key`) VALUES (4, '%s')" % emoji_item

connection = pymysql.connect(host='127.0.0.1', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()
finally:
    connection.close()
