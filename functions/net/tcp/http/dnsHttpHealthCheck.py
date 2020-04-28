#!/usr/bin/python
# coding=utf-8

import httplib

import dns.resolver

ip_address_list = []  # define domain name ip_address list variable
domain_name = "www.taobao.com"  # define service domain name


# domain name resolution function, if resolve successful then append to ip_addressList
def get_ip_address_list(domain=""):
    try:
        record_a = dns.resolver.query(domain, 'A')  # A recode type
    except Exception, e:
        print "dns resolver error:" + str(e)
        return
    for ip in record_a.response.answer[-1].items:
        ip_address_list.append(ip.address)
    return True


def check_http_80_service(ip_address):
    check_url = ip_address + ":80"
    get_content = ""
    httplib.socket.setdefaulttimeout(5)  # define http connection timeout(default 5s)
    conn = httplib.HTTPConnection(check_url)  # create connection object

    try:
        conn.request("GET", "/", headers={"Host": domain_name})  # A URL request, add the host host header
        r = conn.getresponse()
        get_content = r.read(15)  # To obtain 15 characters in the URL page, in order to do the availability check
    finally:
        # Monitor the content of the page URL is commonly defined in advance, such as "HTTP200" and so on
        if get_content != "":
            print ip_address + " [OK]"
        else:
            print ip_address + " [Error]"  # Here to put the alarm procedures, can be E-mail, SMS notification


if __name__ == "__main__":
    if get_ip_address_list(domain_name) and len(
            ip_address_list) > 0:  # Condition: DNS correctly and to return to at least one ip_address
        for current_ip_address in ip_address_list:
            check_http_80_service(current_ip_address)
    else:
        print "dns resolver error."
