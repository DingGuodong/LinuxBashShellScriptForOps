#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:sampleHTTPServerOverFlask.py
User:               Guodong
Create Date:        2017/3/20
Create Time:        19:14
 """
from flask import Flask, request

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/', methods=['GET', 'POST'])
def response_root():
    if request.method == 'GET':
        return "GET"
    elif request.method == 'POST':
        if is_valid_login(request.form['token']):
            return "POST"
        else:
            return 'Invalid token'
    else:
        return "Not Implemented Error"


@app.route('/favicon.ico')
def response_favicon():
    pass


def is_valid_login(token):
    if token == "SDbsugeBiC58A":
        return True
    else:
        return False


def get_local_ip_address():
    import netifaces
    routingIPAddr = '127.0.0.1'
    for interface in netifaces.interfaces():
        if interface == netifaces.gateways()['default'][netifaces.AF_INET][1]:
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            except KeyError:
                pass
    return routingIPAddr


if __name__ == '__main__':
    ip = get_local_ip_address()
    app.debug = True
    app.run(host=ip, port=80)
