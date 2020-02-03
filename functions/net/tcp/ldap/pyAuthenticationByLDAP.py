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
                    https://www.python-ldap.org/en/latest/reference/index.html

                    Learn from "LDAP Admin":
                        Fetch DNs --> Base: DC=aliyun,DC=com
                        Auth:
                            Simple authentication: SSL,TLS
                            GSS-API: SASL
                    known issue:
                        Q: SERVER_DOWN: {'info': u'error:1416F086:SSL routines:tls_process_server_certificate:
                        certificate verify failed (self signed certificate in certificate chain)',
                        'desc': u"Can't contact LDAP server"}
                        A:
Prerequisites:      pip2.7 install --upgrade pip
                    pip2.7 install -U certifi
                    python-ldap (for windows)
                    https://www.python-ldap.org/en/latest/installing.html
                    [Unofficial Windows Binaries for Python Extension Packages]
                    (http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap)
                    Attention: python 64bit need 64bit whl package.
                    pip install https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/python_ldap-3.1.0-cp27-cp27m-win_amd64.whl

 """
import certifi
import ldap

CA_CERT_FILE = certifi.where()


class LDAPAuthentication(object):
    def __init__(self, debug_level=0):
        self.debug_level = debug_level if debug_level >= 0 else 0  # can be 0, 2, 9

        self.schema = "ldap"
        self.uri = None
        self.ldap_host = None
        self.ldap_port = None

        self.ldap_enable_ssl = True  # SSL

        # STRONG_AUTH_REQUIRED: {'info': u'please use starttls', 'desc': u'Strong(er) authentication required'}
        self.ldap_enable_tls = False  # use starttls

        self.ldap_user = None
        self.ldap_password = None
        self.conn = None
        self.is_active = False
        self.ldap_base_dn = None
        self.user_data = None

    def connect(self, host, port, enable_tls=False, enable_ssl=False):
        self.ldap_host = host
        self.ldap_port = str(port)

        ldap.set_option(ldap.OPT_PROTOCOL_VERSION, ldap.VERSION3)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap.set_option(ldap.OPT_REFERRALS, 0)  # this option is required in Windows Server 2012

        if self.ldap_port == "636":
            enable_ssl = True
        if enable_ssl:
            self.schema = "ldaps"
            self.ldap_enable_ssl = True
        else:
            self.schema = "ldap"

        self.uri = self.schema + "://" + self.ldap_host + ":" + self.ldap_port
        self.conn = ldap.initialize(self.uri, trace_level=self.debug_level)

        if enable_tls:
            self.ldap_enable_tls = True
            self.conn.set_option(ldap.OPT_X_TLS_CACERTFILE, CA_CERT_FILE)
            self.conn.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
            self.conn.set_option(ldap.OPT_X_TLS_DEMAND, True)
            self.conn.set_option(ldap.OPT_DEBUG_LEVEL, 255)
            self.conn.start_tls_s()

    def login(self, username, password):
        self.ldap_user = username
        self.ldap_password = password

        if self.conn is None:
            raise Exception("self defined output is: authentication required")

        try:
            if self.ldap_enable_ssl or self.ldap_enable_tls:
                # self.conn.set_option(ldap.OPT_X_TLS_CACERTDIR, 'C:\\Python27\\lib\\site-packages\\certifi')
                result = self.conn.simple_bind_s(who=self.ldap_user, cred=self.ldap_password)
            else:
                result = self.conn.simple_bind(who=self.ldap_user, cred=self.ldap_password)
        except ldap.INVALID_CREDENTIALS as e:
            print(e)
            raise Exception("Invalid credentials")
        except ldap.SERVER_DOWN as e:
            print(e)
            raise Exception("Can't contact LDAP server")

        if result == 1:
            raise Exception("self defined output is: Can't connect to LDAP server , auth failed")
        else:
            if self.debug_level > 0:
                print("self defined output is: " + result)

        self.is_active = True

    def is_authenticated(self):
        if self.is_active is True:
            return True
        else:
            return False

    def get_user_data(self, ldap_base_dn):
        self.ldap_base_dn = ldap_base_dn
        self.user_data = self.conn.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE,
                                            'userPrincipalName=' + self.ldap_user)
        # self.user_data = self.conn.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE)

    def disconnect(self):
        self.conn.unbind()

    def get_distinguishedName(self):
        if self.user_data is not None:
            return self.user_data[0][0]

    def get_userDefinedVar_Mail(self):
        if self.user_data is not None:
            return self.user_data[0][1].get('mail')[0]

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
    hostname = "ldap.mxhichina.com"
    base_dn = "DC=aliyun,DC=com"
    port_tls = 389
    port_ssl = 636
    email = "chris.ding@example.com"
    email_password = "your password here"

    my_ldap = LDAPAuthentication(debug_level=0)
    # my_ldap.connect(hostname, port_tls, enable_tls=True)
    my_ldap.connect(hostname, port_ssl, enable_ssl=True)
    my_ldap.login(email, email_password)
    my_ldap.get_user_data(base_dn)
    print my_ldap.uri
    if my_ldap.is_authenticated():
        print my_ldap.user_data
        print my_ldap.get_distinguishedName()
        print my_ldap.get_userDefinedVar_Mail()
        print my_ldap.get_displayName()
        # print my_ldap.get_userPrincipalName()
        # print my_ldap.get_sAMAccountName()
        # print my_ldap.get_name()
    my_ldap.disconnect()
