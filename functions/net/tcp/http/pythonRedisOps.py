#
# Find package: https://pypi.python.org/pypi
# Refer: http://redis.io/clients#python
# Usage: https://github.com/andymccurdy/redis-py
import redis
import random

redis_host = '123.56.234.219'
redis_port = 6379
redis_password = '6d78247b460acc6bf1d9263e14382fea'
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
value_test = random.randint(0, 99)
value_test = random.randrange(0, 101, 2)
value_test = random.choice('abcdefg&#%^*f')
r.set('foo', value_test)
content = r.get('foo')
print content
r.delete('foo')
