# https://pypi.python.org/pypi?%3Aaction=search&term=curl&submit=search
# pip install pycurl
import curl  # Note: choose 'pycurl' is better

# target_url = 'http://www.google.com.hk'
target_url = 'http://www.baidu.com/'
p = curl.Curl()
p.set_timeout(5)
p.set_url(target_url)
p.get()
print p.header()
print p.info()
print p.info().get('response-code')
print p.info().get('namelookup-time')
print p.info().get('connect-time')
print p.info().get('pretransfer-time')
print p.info().get('starttransfer-time')
print p.info().get('total-time')

print p.info().get('size-download')
print p.info().get('header-size')
print p.info()['speed-download']

p.close()
