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
| character_set_client     | utf8mb4                                                 |
| character_set_connection | utf8mb4                                                 |
| character_set_database   | utf8                                                    |
| character_set_filesystem | binary                                                  |
| character_set_results    | utf8mb4                                                 |
| character_set_server     | utf8                                                    |
| character_set_system     | utf8                                                    |
| character_sets_dir       | C:\Program Files\MySQL\MySQL Server 5.6\share\charsets\ |
+--------------------------+---------------------------------------------------------+
8 rows in set (0.05 sec)

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


# Table structure for emoji_utf8
----------------------------------------------------------------------------------------------------
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for emoji_utf8
-- ----------------------------
DROP TABLE IF EXISTS `emoji_utf8`;
CREATE TABLE `emoji_utf8`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;


# Table structure for emoji_utf8_all
----------------------------------------------------------------------------------------------------
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for emoji_utf8_all
-- ----------------------------
DROP TABLE IF EXISTS `emoji_utf8_all`;
CREATE TABLE `emoji_utf8_all`  (
  `id` int(11) NOT NULL,
  `key` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;


Conclusion & Summary:
----------------------------------------------------------------------------------------------------
1. uft8mb4 in MySQL is real utf8 in Python

2. If you want get right emoji:
    a. make sure character_set_client, character_set_connection and character_set_results are utf8mb4.
    b. make sure the field in table or the table using utf8mb4 as character and collate set

3. You will get right emoji even MySQL table using utf8 as character and collate set but the field using utf8mb4.
 """
import pymysql


def get_current_char_setting_using_utf8mb4():
    sql = 'show variables like "%char%";'

    # charset will effect "character_set_client, character_set_connection, character_set_results"
    connection = pymysql.connect(host='127.0.0.1', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            if cursor is not None:
                results = cursor.fetchall()  # <type 'list'>
                for result in results:
                    print(result.get("Variable_name"), result.get("Value"))
        connection.commit()
    finally:
        connection.close()


def emoji_utf8bm4_crud():
    # emoji_item = u'\U0001f604'.encode('utf-8')  # '😄', b'\xf0\x9f\x98\x84' in 'utf-8'
    emoji_item = u'\U0001f604' or '😄'  # '😄', u'\U0001f604' ==  '😄' in python3
    sql = "INSERT INTO `test`.`emoji`( `key`) VALUES ('%s')" % emoji_item

    connection = pymysql.connect(host='127.0.0.1', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()


def emoji_utf8_crud_test():
    # emoji_item = u'\U0001f604'.encode('utf-8')  # '😄'
    emoji_item = '😄'  # '😄'
    sql = "INSERT INTO `test`.`emoji_utf8`(`key`) VALUES ('%s')" % emoji_item

    connection = pymysql.connect(host='127.0.0.1', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()


def emoji_utf8_all_crud_test():
    # emoji_item = u'\U0001f604'.encode('utf-8')  # '😄'
    emoji_item = '😄'  # '😄'
    sql = "INSERT INTO `test`.`emoji_utf8_all`(`key`) VALUES ('%s')" % emoji_item

    connection = pymysql.connect(host='127.0.0.1', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()


if __name__ == '__main__':
    get_current_char_setting_using_utf8mb4()
    emoji_utf8bm4_crud()  # successful
    emoji_utf8_crud_test()  # successful
    emoji_utf8_all_crud_test()  # failed
