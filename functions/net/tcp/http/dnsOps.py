import os

try:
    import dns.resolver
except ImportError:
    try:
        command_to_execute = "pip install dnspython"
        os.system(command_to_execute)
    except OSError:
        exit(1)
import dns.resolver

# domain = raw_input("Please input a domain name: ")
domain = "www.baidu.com"
A = dns.resolver.query(domain, 'A')
for i in A.response.answer:
    for j in i.items:
        print j

cname = dns.resolver.query(domain, 'CNAME')
for i in cname.response.answer:
    for j in i.items:
        print j.to_text()

result = dns.resolver.query(domain, dns.rdatatype.A, dns.rdataclass.IN)
for i in result.response.answer:
    print i
