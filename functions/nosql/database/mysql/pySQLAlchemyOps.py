#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pySQLAlchemyOps.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/3/7
Create Time:            16:08
Description:            SQLAlchemy
Long Description:       a very simple example of using SQLAlchemy( SQL /'ælkəmi/)
References:             http://www.sqlalchemy.org/library.html#reference
Prerequisites:          pip install sqlalchemy
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
from sqlalchemy import String, Column, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DBConfigDict = {
    "is_enable": False,
    "driver": "mysql+pymysql",
    "host": "127.0.0.1",
    "port": 3306,
    "user": "dev",
    "password": "dEvp@ssw0rd",
    "database": "test",
    "charset": 'utf8mb4'
}

dialect_url = '{driver}://{user}:{password}@{host}/{dbname}?charset={charset}'.format(
    driver=DBConfigDict.get('driver'),
    user=DBConfigDict.get('user'),
    password=DBConfigDict.get('password'),
    host=DBConfigDict.get('host'),
    dbname=DBConfigDict.get('database'),
    charset=DBConfigDict.get('charset'),
)

# dialect+driver://username:password@host:port/database
# mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
# engine = sqlalchemy.create_engine("mysql://dev:dEvp@ssw0rd@localhost/test?charset=utf8")
engine = create_engine(dialect_url)
Session = sessionmaker(bind=engine)

# execute a RAW SQL
with engine.connect() as con:
    rs = con.execute("SELECT VERSION()")
    print(rs.fetchone())

Base = declarative_base()


class Emoji(Base):
    __tablename__ = "Emoji"
    mysql_engine = 'InnoDB'
    mysql_charset = 'utf8mb4'  # optional

    Id = Column("id", Integer, nullable=False, primary_key=True)
    Key = Column("key", String(255))

    def __init__(self, _id, value):
        self.Id = _id
        self.Key = value

    def __repr__(self):
        return self.__tablename__


# initialize object, use this instance to CRUD
session = Session()

print session.query(Emoji.Id, Emoji.Key).all()

# select
print session.query(Emoji.Id, Emoji.Key).filter_by(Id=1).all()
print session.query(Emoji.Id, Emoji.Key).filter(Emoji.Id == 1).all()

# insert
new_record = Emoji(6, u'\U0001f604')  # insert a new record '😄'
if session.query(Emoji.Id).filter_by(Id=6).first() is None:
    session.add(new_record)
    session.commit()

# delete
record = session.query(Emoji).get(6)
if record is not None:
    print record.Id, record.Key
    session.delete(new_record)
    session.commit()

# update
session.query(Emoji).get(1).Key = u'\U0001f44c'  # set a new value '👌'
print session.query(Emoji.Id, Emoji.Key).all()
session.query(Emoji).get(1).Key = u'test1'  # roll back
