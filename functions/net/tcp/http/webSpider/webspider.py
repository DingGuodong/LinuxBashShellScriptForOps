import os
import random

try:
    import requests
except ImportError:
    try:
        print "requests model is not installed, try install it ..."
        command_to_execute = "pip install requests"
        os.system(command_to_execute)
    except OSError:
        exit(1)
    finally:
        import requests

url = 'http://dgd2010.blog.51cto.com/1539422/1784390'
fake_content_list = ["index.php", '%3F', "%091464773814", "%09", "%2F"]
fake_content = random.shuffle(fake_content_list)
cookies = dict(lastvisit=fake_content)
print cookies
r = requests.get(url, cookies=cookies)
print r.status_code
print r.encoding
print r.cookies
print r.cookies['lastvisit']
