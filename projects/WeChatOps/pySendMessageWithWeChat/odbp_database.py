#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:odbp_database.py.py
User:               Guodong
Create Date:        2016/8/15
Create Time:        14:30
 """
import os
import sqlite3
import sys

# import time

enable_debug = True


def debug(msg, code=None):
    if enable_debug:
        if code is None:
            print "message: %s" % msg
        else:
            print "message: %s, code: %s " % (msg, code)


AUTHOR_MAIL = "uberurey_ups@163.com"

weixin_qy_CorpID = "wx4dd961cd206edb07"
weixin_qy_Secret = "UZ4e4jCFHySnH6i3X8Ayr-aHvoUhAFhH6yrMI6qnmtGZnIWrEIM7PTEHPvaf30zD"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '.odbp_db.sqlite3'),
    }
}

sqlite3_db_file = str(DATABASES['default']['NAME'])


def sqlite3_conn(database):
    try:
        conn = sqlite3.connect(database)
    except sqlite3.Error:
        print >> sys.stderr, """\
    There was a problem connecting to Database:

        %s

    The error leading to this problem was:

        %s

    It's possible that this database is broken or permission denied.

    If you cannot solve this problem yourself, please mail to:

        %s

    """ % (database, sys.exc_value, AUTHOR_MAIL)
        sys.exit(1)
    else:
        return conn


def sqlite3_commit(conn):
    return conn.commit()


def sqlite3_close(conn):
    return conn.close()


def sqlite3_execute(database, sql):
    try:
        sql_conn = sqlite3_conn(database)
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute(sql)
        sql_conn.commit()
        sql_conn.close()
    except sqlite3.Error as e:
        print e
        sys.exit(1)


def sqlite3_create_table_token():
    sql_conn = sqlite3_conn(sqlite3_db_file)
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute('''CREATE TABLE "main"."weixin_token" (
                "id"  INTEGER ,
                "access_token"  TEXT,
                "expires_in"  TEXT,
                "expires_on"  TEXT,
                "is_expired"  INTEGER
                )
                ;
    ''')
    sqlite3_commit(sql_conn)
    sqlite3_close(sql_conn)


def sqlite3_create_table_account():
    sql_conn = sqlite3_conn(sqlite3_db_file)
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute('''CREATE TABLE "main"."weixin_account" (
                "id"  INTEGER,
                "name"  TEXT,
                "corpid"  TEXT,
                "secret"  TEXT,
                "current"  INTEGER
                )
                ;
    ''')
    sqlite3_commit(sql_conn)
    sqlite3_close(sql_conn)


def sqlite3_create_table_limits():
    sql_conn = sqlite3_conn(sqlite3_db_file)
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute('''CREATE TABLE "main"."weixin_limit" (
                "id"  INTEGER PRIMARY KEY ,
                "limit"  INTEGER,
                "used"  INTEGER,
                "datetime"  TEXT
                )
                ;
    ''')
    sqlite3_commit(sql_conn)
    sqlite3_close(sql_conn)


def sqlite3_create_tables():
    pass


def sqlite3_set_credential(corpid, secret):
    try:
        sql_conn = sqlite3_conn(sqlite3_db_file)
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute('''INSERT INTO "weixin_account" ("id", "name", "corpid", "secret", "current") VALUES
                                (1,
                                'odbp',
                                ?,
                                ?,
                                1)
''', (corpid, secret))
        sqlite3_commit(sql_conn)
        sqlite3_close(sql_conn)
    except sqlite3.Error:
        sqlite3_create_table_account()
        sqlite3_set_credential(corpid, secret)


def sqlite3_set_token(access_token, expires_in, expires_on, is_expired):
    try:
        sql_conn = sqlite3_conn(sqlite3_db_file)
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute('''INSERT INTO "weixin_token"
                              ("id", "access_token", "expires_in", "expires_on", "is_expired") VALUES
                              (
                              1,
                              ?,
                              ?,
                              ?,
                              ?
                              )
''', (access_token, expires_in, expires_on, is_expired))
        sqlite3_commit(sql_conn)
        sqlite3_close(sql_conn)
    except sqlite3.Error:
        sqlite3_create_table_token()
        sqlite3_set_token(access_token, expires_in, expires_on, is_expired)


def sqlite3_set_limit(limit, used, datetime):
    try:
        sql_conn = sqlite3_conn(sqlite3_db_file)
        sql_cursor = sql_conn.cursor()
        sql_cursor.execute('''INSERT INTO "weixin_limit"
                              ("id", "limit", "used", "datetime") VALUES
                              (
                              1,
                              ?,
                              ?,
                              ?
                              )
''', (limit, used, datetime))
        sqlite3_commit(sql_conn)
        sqlite3_close(sql_conn)
    except sqlite3.Error:
        sqlite3_create_table_limits()
        sqlite3_set_limit(limit, used, datetime)


def sqlite3_get_credential():
    try:
        sql_conn = sqlite3_conn(sqlite3_db_file)
        sql_cursor = sql_conn.cursor()
        credential = sql_cursor.execute('''SELECT "corpid", "secret"  FROM weixin_account WHERE current = 1;''')
        result = credential.fetchall()
        sqlite3_close(sql_conn)
    except sqlite3.Error:
        sqlite3_set_credential(weixin_qy_CorpID, weixin_qy_Secret)
        return sqlite3_get_credential()
    else:
        if result is not None:
            return result
        else:
            print "unrecoverable problem, please alter to %s" % AUTHOR_MAIL
            sys.exit(1)


def sqlite3_get_token():
    try:
        sql_conn = sqlite3_conn(sqlite3_db_file)
        sql_cursor = sql_conn.cursor()
        credential = sql_cursor.execute(
            '''SELECT "access_token", "expires_on" FROM weixin_token WHERE "is_expired" = 1 ;''')
        result = credential.fetchall()
        sqlite3_close(sql_conn)
    except sqlite3.Error:
        info = sys.exc_info()
        print info[0], ":", info[1]
    else:
        if result is not None:
            return result
        else:
            # print "unrecoverable problem, please alter to %s" % AUTHOR_MAIL
            # sys.exit(1)
            return None


def sqlite3_get_limits():
    result = None
    try:
        sql_conn = sqlite3_conn(sqlite3_db_file)
        sql_cursor = sql_conn.cursor()
        limit = sql_cursor.execute(
            '''SELECT "used", "datetime" FROM weixin_limit WHERE _ROWID_ = 1 ;''')
        result = limit.fetchall()
        sqlite3_close(sql_conn)
    except sqlite3.Error:
        try:
            sqlite3_create_table_limits()
        except sqlite3.Error:
            pass
    if result is not None and len(result) != 0:
        return result
    else:
        # print "unrecoverable problem, please alter to %s" % AUTHOR_MAIL
        # sys.exit(1)
        return None


def sqlite3_update_token(access_token, expires_on):
    sql_conn = sqlite3_conn(sqlite3_db_file)
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute('''UPDATE "weixin_token" SET
                          access_token=?,
                          expires_on=?
                          WHERE _ROWID_ = 1;''', (access_token, expires_on)
                       )
    sqlite3_commit(sql_conn)
    sqlite3_close(sql_conn)


def sqlite3_update_account(new_corpid, new_secret):
    sql_conn = sqlite3_conn(sqlite3_db_file)
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute('''UPDATE "weixin_account" SET
                          corpid=?,
                          secret=?
                          WHERE _ROWID_ = 1;''', (new_corpid, new_secret)
                       )
    sqlite3_commit(sql_conn)
    sqlite3_close(sql_conn)


def sqlite3_update_limit(new_used, new_datetime):
    sql_conn = sqlite3_conn(sqlite3_db_file)
    sql_cursor = sql_conn.cursor()
    sql_cursor.execute('''UPDATE "weixin_limit" SET
                          used=?,
                          datetime=?
                          WHERE _ROWID_ = 1;''', (new_used, new_datetime)
                       )
    sqlite3_commit(sql_conn)
    sqlite3_close(sql_conn)
