#!/usr/bin/env bash

# centos, yum info xml2
#Available Packages
#Name        : xml2
#Arch        : x86_64
#Version     : 0.5
#Release     : 7.el6
#Size        : 22 k
#Repo        : epel
#Summary     : XML/Unix Processing Tools
#URL         : http://dan.egnor.name/xml2/
#License     : GPLv2+
#Description : These tools are used to convert XML and HTML to and from a
#            : line-oriented format more amenable to processing by classic Unix
#            : pipeline processing tools, like grep, sed, awk, cut, shell scripts,
#            : and so forth.

# debian/ubuntu, apt-cache show xml2
#Description-en: Convert between XML, HTML, CSV and a line-oriented format
#               xml2 tools are used to convert XML, HTML and CSV to and from a
#               line-oriented format more amenable to processing by classic Unix
#               pipeline processing tools, like grep, sed, awk, cut, shell scripts,
#               and so forth.
# for xmllint, sudo apt install libxml2-utils
which xmllint || sudo apt install -y libxml2-utils || yum install -y libxml2-utils
# for xml2, sudo apt install xml2
which xml2 || sudo apt install -y xml2 || yum install -y xml2

cat >d.xml<<'eof'
<?xml version="1.0" encoding="UTF-8"?>
<Result>
    <Error>8</Error>
    <Failure>5</Failure>
</Result>
eof

xml2 < d.xml

xml2 < d.xml | grep '/Result/Error'|sed 's/.*=//g'

rm -f d.xml
