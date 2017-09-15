#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyAuthenticationByLDAP.py
User:               Guodong
Create Date:        2017/9/14
Create Time:        15:01
Description:        Python LDAP (ActiveDirectory) authentication
                    Verifies credentials for username and password.
References:         [Python LDAP (ActiveDirectory) authentication](https://gist.github.com/ibeex/1288159)
        `           [Flask Authentication With LDAP]
                    (https://code.tutsplus.com/tutorials/flask-authentication-with-ldap--cms-23101)
                    [LDAP & LDAPS URLs](http://docs.oracle.com/javase/jndi/tutorial/ldap/misc/url.html)
Prerequisites:      python-ldap (for windows)
                    [Unofficial Windows Binaries for Python Extension Packages]
                    (http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap)
                    Attention: python 64bit need 64bit whl package.

 """
import ldap


class LDAPAuthentication(object):
    def __init__(self, username, password):
        ldap_host = "192.168.78.8"
        ldap_port = "389"
        ldaps_port = "636"
        ldap_enable_ldaps = False
        self.ldap_base_dn = "DC=example,DC=com,DC=cn"  # example.com.cn

        self.ldap_user = username
        self.ldap_password = password

        if ldap_enable_ldaps is True:
            self.uri = "ldaps://" + ldap_host + ":" + ldaps_port
        else:
            self.uri = "ldap://" + ldap_host + ":" + ldap_port

        self.is_active = False
        self.user_data = None

        self.conn = ldap.initialize(self.uri)

        try:
            self.conn.simple_bind_s(who=self.ldap_user, cred=self.ldap_password)
            # print conn.search_s(ldap_base_dn, ldap.SCOPE_SUBTREE)
            self.is_active = True
            self.user_data = self.conn.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE,
                                                'userPrincipalName=' + self.ldap_user)
        except ldap.INVALID_CREDENTIALS:
            raise Exception("Invalid credentials")
        except ldap.SERVER_DOWN:
            raise Exception("Can't contact LDAP server")

    def is_authenticated(self):
        if self.is_active is True:
            return True
        else:
            return False

    def get_distinguishedName(self):
        if self.user_data is not None:
            return self.user_data[0][0]

    def get_userPrincipalName(self):
        if self.user_data is not None:
            return self.user_data[0][1]['userPrincipalName'][0]

    def get_sAMAccountName(self):
        if self.user_data is not None:
            return self.user_data[0][1]['sAMAccountName'][0]

    def get_displayName(self):
        if self.user_data is not None:
            return self.user_data[0][1]['displayName'][0]

    def get_name(self):
        if self.user_data is not None:
            return self.user_data[0][1]['name'][0]


if __name__ == '__main__':
    u = LDAPAuthentication("chris.ding@another-example.cn", "your password here")
    print u.is_authenticated()
    print u.get_distinguishedName()
    print u.get_userPrincipalName()
    print u.get_sAMAccountName()
    print u.get_displayName()
    print u.get_name()
