# https://pypi.python.org/pypi?%3Aaction=search&term=curl&submit=search
# pip install pycurl
import curl

# target_url = 'http://www.google.com.hk'
target_url = 'http://www.baidu.com/'
p = curl.Curl()
p.set_timeout(5)
p.set_url(target_url)
p.get()
print p.header()
