import cookielib
import urllib2
import urllib

# http://cuiqingcai.com/968.html

username = ""
password = ""

# first url request
baiduSpaceEntryUrl = "http://hi.baidu.com/motionhouse"
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
resp = urllib2.urlopen(baiduSpaceEntryUrl)

for item in cookie:
    print type(item)

exit(1)
# second time do url request, the CookieJar will auto handle the cookie
loginBaiduUrl = "https://passport.baidu.com/?login"
para = {
    'username': username,
    'password': password,
    'mem_pass': 'on',
}
postData = urllib.urlencode(para)
req = urllib2.Request(loginBaiduUrl,
                      postData)  # urllib2.Request: the HTTP request will be a POST instead of a GET when the data parameter is provided.
req.add_header('User-Agent',
               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
req.add_header('Cache-Control', 'no-cache')
req.add_header('Accept', '*/*')
req.add_header('Connection', 'Keep-Alive')
resp = urllib2.urlopen(req)
respInfo = resp.info()
respRead = resp.read()

print respInfo

print respRead

