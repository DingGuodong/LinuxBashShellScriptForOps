#!/usr/bin/python3

# [Retrying library for Python](https://github.com/jd/tenacity)
# Tenacity is a library that provides a decorator and context manager that retries a function or method until it returns a result or raises an exception.
import time
import random
from tenacity import retry, stop_after_delay, stop_after_attempt, wait_fixed

@retry(wait = wait_fixed(2), stop=(stop_after_delay(3) | stop_after_attempt(5)))
def do_action():
    time.sleep(random.random())
    print(f'spent {time.time() - start_time} seconds')
    
    raise Exception

if __name__ == '__main__':
    start_time = time.time()
    do_action()
