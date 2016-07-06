#!/usr/bin/python
#
# Copyright (C) 2011-2012
#
# Douglas Schilling Landgraf <dougsland@gmail.com>
#
# python-confparser - A KISS python module to parse *nix config files
# https://github.com/dougsland/python-confparser/blob/master/confparser.py
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301
# USA

import os
import sys
import getpass
import shutil
import datetime

# DEFAULT PATH to python-confparser
CONFPARSE_PATH = "/home/" + getpass.getuser() + "/.python-confparser"

# FORMAT TO WRITE
CONFSTRING = 0
CONF_STRING = 0
CONF_NO_STRING = 1
CONF_NOT_STRING = 1
CONFNUMBER = 2
VERSION = "1.0.2"


def setConfValue(pathFile, confName, newValue, typeData):
    retSetConf = ""
    found = -1
    newConfFile = pathFile + ".new"

    try:
        CURRENT_FILE = open(pathFile, 'r')
    except IOError, reason:
        print "cannot find config file: {0}\n{1}".format(pathFile, reason)
        sys.exit(-1)

    try:
        NEW_FILE = open(newConfFile, 'w')
    except IOError, reason:
        print "cannot create config file: {0}\n{1}".format(pathFile, reason)
        sys.exit(-1)

    while True:
        line = CURRENT_FILE.readline()
        ret = line.find(confName)
        if ret != -1:
            # Writing the new value
            if (typeData == CONF_NO_STRING) or (typeData == CONFNUMBER) \
                    or (typeData == CONF_NO_STRING):
                # DO NOT include " "
                NEW_FILE.write("{0} = {1}".format(confName, newValue))
                NEW_FILE.write("\n")
            # special entry - put between the " other caracter
            else:
                # Writing string - including " "
                NEW_FILE.write("{0} = \"{1}\"".format(confName, newValue))
                NEW_FILE.write("\n")

            # finish the job
            # raising flags retSetConf = 0 (OK) and found = 0 (OK)
            retSetConf = 0
            found = 0
        else:
            NEW_FILE.write(line)
        # len = 0 - No more lines to read (EOF)
        if len(line) == 0:
            break

    # The configuration not found? return the string "confNotFound"
    if retSetConf == "" and found == -1:
        # Writing the new value
        if typeData == CONFNUMBER:
            # Writing number DO NOT INCLUDE " "
            NEW_FILE.write("{0} = {1}".format(confName, newValue))
            NEW_FILE.write("\n")

        # special entry - put between the " other caracter
        else:
            # Writing string - including " "
            NEW_FILE.write("{0} = \"{1}\"".format(confName, newValue))
            NEW_FILE.write("\n")

        # finish the job - raising flags retSetConf = 0 (OK) and found = 0 (OK)
        retSetConf = 0
        found = 0

    CURRENT_FILE.close()
    NEW_FILE.close()

    # if python-confparser path doesn't exist, create the dir
    if not os.path.exists(CONFPARSE_PATH):
        os.mkdir(CONFPARSE_PATH)

    # copying the old file to the .python-confparser dir
    now = datetime.datetime.now()
    fname = pathFile.split('/')

    # fname [-1] = last item of list (name of file)
    shutil.copy(pathFile, (
        CONFPARSE_PATH + "/" + fname[-1] + "-" + now.strftime(
            "%Y-%m-%d_%H-%M")))

    # removing the previous file
    os.remove(pathFile)

    # renaming the current config
    shutil.move(newConfFile, pathFile)

    return retSetConf


def getConfValue(pathFile, confName):
    confValue = ""
    found = -1

    try:
        FILE = open(pathFile).readlines()
    except IOError, reason:
        print "cannot locate configuration file: %s" % pathFile
        sys.exit(-1)

    for line in [l.strip() for l in FILE]:
        if not line:
            continue

        ret = line.find(confName)
        if ret != -1:
            # configuration commented? return value is #
            if line[0] == "#":
                confValue = "confCommented"
            else:
                confValue = ""
                sizeString = len(line)
                indexEqual = line.index('=')
                indexEqual += 1  # Get next caracter from =

                for i in range(indexEqual, sizeString):
                    if (line[i] == "\"") or (line[i] == " "):
                        continue
                    confValue += line[i]
                    # we have found the conf - raising flag found = 0 (OK)
                    found = 0

    # The configuration not found? return the string "confNotFound"
    if confValue == "" and found == -1:
        confValue = "confNotFound"

    return confValue


def confToDict(pathFile):
    var = {}

    try:
        FILE = open(pathFile, 'r+')
    except IOError, reason:
        print "cannot find configuration" \
              "file: {0}\n{1}".format(pathFile, reason)
        sys.exit(-1)

    while True:

        # cleaning variables
        cleanConfValue = ""
        cleanConfName = ""
        confName = ""
        confValue = ""
        confStatus = ""
        typeAttribute = "NoAttr"

        line = FILE.readline()
        ret = line.find("=")
        if ret != -1:
            if line[0] == "#":
                confStatus = "commented"
            else:
                confStatus = "activated"

            conf = line.split('=')

            # conf[0] = confName - conf[1] = confValue
            confName = conf[0]
            confValue = conf[1]

            # Cleaning the confName
            sizeString = len(conf[0])
            for i in range(0, sizeString):
                if (confName[i] == "#") or (confName[i] == "\n"):
                    continue
                cleanConfName += confName[i]

            # Cleaning the confValue - removing " or spaces
            sizeString = len(conf[1])
            print "sizeString ->" + str(sizeString)
            print "conf[1] -> " + conf[1]
            for i in range(0, sizeString):

                if (i == 0) and (confValue[i] == "\"") or \
                                (i == 1) and (confValue[i] == "\""):
                    typeAttribute = "string"
                    continue

                if (i == 1) and (confValue[i] != "\""):
                    typeAttribute = "no string"

                """
                # removing space from numbers
                if not typeAttribute == "string":
                    if (confValue[i] == " ") or
                           (confValue[i] == "\n") or (confValue[i] == "\""):
                        continue

                    if confValue[i] == "#":
                        break
                else:
                    if (confValue[i] == "\n") or (confValue[i] == "\""):
                        continue

                cleanConfValue += confValue[i]
                """
            cleanConfValue = conf[1].strip("\n")

            if typeAttribute == "NoAttr":
                typeAttribute = "no string"

            # print cleanConfValue
            # print typeAttribute
            # appending to the dict
            # print "->1" + cleanConfName
            # print "->2" + cleanConfValue
            u = {cleanConfName.strip(): cleanConfValue, (
                cleanConfName.strip() + '_status'): confStatus,
                 (cleanConfName.strip() + '_type'): typeAttribute,
                 (cleanConfName.strip() + '_key'): cleanConfName}

            # print u
            var.update(u)

        # len = 0 - No more lines to read (EOF)
        if len(line) == 0:
            break

    print str(var)
    FILE.close()
    return var


def getNumberOfElementsInDict(var):
    # multiple of 4, since we create for each element three
    # additional keys (type, key, status)
    return len(var.keys()) / 4


def getConfParserVersion():
    return getConfparserVersion()


def getConfparserVersion():
    return VERSION


def writeDictToFile(pathFile, var):
    newConfFile = pathFile + ".new"

    # if python-confparser path doesn't exist, create the dir
    if not os.path.exists(CONFPARSE_PATH):
        os.mkdir(CONFPARSE_PATH)

    # copying the old file to the .python-confparser dir
    now = datetime.datetime.now()
    fname = pathFile.split('/')

    # fname [-1] = last item of list (name of file)
    shutil.copy(pathFile, (
        CONFPARSE_PATH + "/" + fname[-1] + "-" + now.strftime(
            "%Y-%m-%d_%H-%M")))

    try:
        CURRENT_FILE = open(pathFile, 'r')
    except IOError, reason:
        print "cannot find configuration" \
              " file: {0}\n{1}".format(pathFile, reason)
        sys.exit(-1)

    try:
        NEW_FILE = open(newConfFile, 'w')
    except IOError, reason:
        print "cannot create new configuration" \
              "file: {0}\n{1}".format(pathFile, reason)
        sys.exit(-1)

    while True:
        AttrCommented = False
        confName = ""
        confValue = ""
        cleanConfName = ""
        cleanConfValue = ""
        lineType = ""

        line = CURRENT_FILE.readline()
        ret = line.find("=")
        if ret != -1:
            conf = line.split('=')
            confName = conf[0]
            confValue = conf[1]

            # Cleaning the confName
            sizeString = len(conf[0])
            # print sizeString
            for i in range(0, sizeString):
                if (confName[i] == "#") or (confName[i] == " ") or (
                            confName[i] == "\n"):
                    continue
                cleanConfName += confName[i]

            # Cleaning the confValue
            sizeString = len(conf[1])
            for i in range(0, sizeString):
                if confValue[i] == "\"":
                    lineType = "string"
                    continue

                if (confValue[i] == "#") or (
                            confValue[i] == " ") or (confValue[i] == "\n"):
                    continue
                cleanConfValue += confValue[i]
                print cleanConfValue

            if lineType != "string":
                lineType = "no string"

            # Setting members of dict
            dictType = cleanConfName + "_type"
            dictStatus = cleanConfName + "_status"
            dictKey = cleanConfName + "_key"

            # Getting the values from dict
            # var.get(mydict_from_argument)
            AttrType = var.get(dictType)
            AttrCommented = var.get(dictStatus)
            AttrValue = var.get(cleanConfName)

            cleanConfName = var.get(dictKey)

            # DEBUG
            """
            if (cleanConfName == "log_outputs"):
                print "line[0] " + line[0]
                print "cleanConfName: "   + cleanConfName
                print "cleanConfValue: "  + cleanConfValue
                print "dict: confName: "  + confName
                print "lineType: "        + lineType
                print "dict: AttrType: "      + AttrType
                # string or no string
                print "dict: AttrCommented: " + AttrCommented
                # commented or activated
                print "dict: AttrValue: "     + AttrValue + "\n"
            """

            # if the current file contain the attribute commented and the
            # dict says it's activated - let's remove the comment
            if (line[0] == "#") and (AttrCommented == "activated"):
                if AttrType == "string":
                    NEW_FILE.write("{0} = \"{1}\"\n".format(
                        cleanConfName, AttrValue))
                else:
                    NEW_FILE.write("{0} = {1}\n".format(
                        cleanConfName, AttrValue))

            # if the attritbute in the current file is not
            # commented and the dict
            # status changed to commented - let's comment
            # the attribute into the .conf
            elif (line[0] != "#") and (AttrCommented == "commented"):
                if AttrType == "string":
                    NEW_FILE.write("#{0}={1}\n".format(
                        cleanConfName, AttrValue))
                else:
                    NEW_FILE.write("#{0}={1}\n".format(
                        cleanConfName, AttrValue))

            elif (lineType == "string") and (
                        AttrType == "no string") or (AttrType == "string") and (
                        lineType == "no string"):
                if (AttrType == "string") and (AttrCommented == "activated"):
                    NEW_FILE.write("{0}={1}\n".format(
                        cleanConfName, AttrValue))
                elif (AttrType == "string") and (
                            AttrCommented == "commented"):
                    NEW_FILE.write("#{0}={1}\n".format(
                        cleanConfName, AttrValue))
                elif (AttrType == "no string") and (
                            AttrCommented == "activated"):
                    NEW_FILE.write("{0}={1}\n".format(
                        cleanConfName, AttrValue))
                elif (AttrType == "no string") and (
                            AttrCommented == "commented"):
                    NEW_FILE.write("#{0}={1}\n".format(
                        cleanConfName, AttrValue))

            # validation if the value changes
            elif cleanConfValue != AttrValue:
                if AttrCommented == "commented" and AttrType == "string":
                    NEW_FILE.write("#{0}={1}\n".format(
                        cleanConfName, AttrValue))
                elif AttrCommented == "commented" and AttrType == "no string":
                    NEW_FILE.write("#{0}={1}\n".format(
                        cleanConfName, AttrValue))
                elif AttrCommented == "activated" and AttrType == "no string":
                    NEW_FILE.write("{0}={1}\n".format(
                        cleanConfName, AttrValue))
                elif AttrCommented == "activated" and AttrType == "string":
                    NEW_FILE.write("{0}={1}\n".format(
                        cleanConfName, AttrValue))
            # No changes, just write the line
            else:
                NEW_FILE.write("{0}".format(line))

        # No equal symbol found in the line, let's write the line
        else:
            NEW_FILE.write("{0}".format(line))

        # len = 0 - No more lines to read (EOF)
        if len(line) == 0:
            break

    NEW_FILE.close()
    CURRENT_FILE.close()

    # removing the previous file
    os.remove(pathFile)

    # renaming the current config
    shutil.move(newConfFile, pathFile)

    return 0
