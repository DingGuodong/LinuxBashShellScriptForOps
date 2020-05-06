#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:password-generator.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/9/19
Create Time:            17:34
Description:            password generator
Long Description:       
References:             Django==1.11.24,
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """

import hashlib
import random
import string
import time
from itertools import repeat

PASSWORD_COMPLEXITY_ONLY_DIGITS = 0  # Only digits
PASSWORD_COMPLEXITY_WITHOUT_CASE = 1  # Case insensitive
PASSWORD_COMPLEXITY_WITH_CASE = 2  # Case sensitive
PASSWORD_COMPLEXITY_WITH_SPECIAL = 3  # Must include special chars


class InvalidPasswordLength(Exception):
    pass


class InvalidPasswordComplexity(Exception):
    pass


class InvalidPasswordMustIncludeLength(Exception):
    pass


# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings

    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False


def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ("%s%s" % (random.getstate(), time.time())).encode('utf-8')
            ).digest())
    return ''.join(random.choice(allowed_chars) for _ in range(length))


def get_random_secret_key():
    """
    Return a 50 character random string usable as a SECRET_KEY setting value.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)


def password_generator(length=7, complexity=3, must_include='.'):
    # type: (int, int, str) -> str
    """
    :param length: password length
    :param complexity: password complexity level
    :param must_include: password must include chars
    :return: str: password
    """
    if length < 7:
        raise InvalidPasswordLength("Invalid password length. Password should be at least 7 digits")
    else:
        length = length - complexity

    if length < len(must_include):
        raise InvalidPasswordMustIncludeLength("Invalid password must include length, "
                                               "length of must_include must less than (length - complexity)")

    if complexity == PASSWORD_COMPLEXITY_WITH_SPECIAL:
        chars = string.letters + string.digits + '!@#$%^&*(-_=+)'  # limited special character
    elif complexity == PASSWORD_COMPLEXITY_WITH_CASE:
        chars = string.letters + string.digits
    elif complexity == PASSWORD_COMPLEXITY_WITHOUT_CASE:
        chars = string.lowercase + string.digits
    elif complexity == PASSWORD_COMPLEXITY_ONLY_DIGITS:
        chars = string.digits
    else:
        raise InvalidPasswordComplexity(
            "Invalid password complexity. "
            "The value of complexity parameter only can be 0, 1, 2 or 3")

    middle_result = get_random_string(length, chars)
    middle_result_list = list(middle_result)

    while True:
        for item in list(must_include):
            pos = random.choice(range(len(middle_result)))
            middle_result_list[pos] = item

        # must include must_include
        for item in list(must_include):
            if item not in middle_result_list:
                break  # break current for loop
        else:
            break  # break while loop

    num_pos = random.choice(range(len(string.digits)))
    lower_pos = random.choice(range(len(string.lowercase)))
    upper_pos = random.choice(range(len(string.uppercase)))
    random_pos1, random_pos2, random_pos3 = repeat(random.choice(range(len(middle_result))), 3)

    if complexity == PASSWORD_COMPLEXITY_WITH_SPECIAL:
        middle_result_list[random_pos1] = middle_result_list[random_pos1] + string.digits[num_pos]
        middle_result_list[random_pos2] = middle_result_list[random_pos2] + string.lowercase[lower_pos]
        middle_result_list[random_pos3] = middle_result_list[random_pos3] + string.uppercase[upper_pos]

    elif complexity == PASSWORD_COMPLEXITY_WITH_CASE:
        middle_result_list[random_pos2] = middle_result_list[random_pos2] + string.lowercase[lower_pos]
        middle_result_list[random_pos3] = middle_result_list[random_pos3] + string.uppercase[upper_pos]

    elif complexity == PASSWORD_COMPLEXITY_WITHOUT_CASE:
        middle_result_list[random_pos1] = middle_result_list[random_pos1] + string.digits[num_pos]

    return ''.join(middle_result_list)


if __name__ == '__main__':
    print(password_generator(7, 0, ''))
    print(password_generator(7, 1, '!'))
    print(password_generator(7, 2, '@'))
    print(password_generator(7, 3, '#'))
    print(password_generator())

    num = 27  # generate 27 passwords
    for _ in range(num):
        print(password_generator(length=16, complexity=3, must_include='@'))
