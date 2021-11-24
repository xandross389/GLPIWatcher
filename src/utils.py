import hashlib
import re
from os import system, name
from datetime import datetime
from random import uniform
from time import sleep

_re_time = re.compile(r'^\s*(?P<hours>\d+?)\s*:\s*(?P<minutes>\d+?)\s*:\s*(?P<seconds>\d+?)\s*$')


def strtime2seconds(str_time):
    res = _re_time.match(str_time)
    if not res:
        raise Exception("El formato del intervalo de tiempo es incorrecto: {}".format(str_time))

    return \
        int(res["hours"]) * 3600 + \
        int(res["minutes"]) * 60 + \
        int(res["seconds"])


def seconds2strtime(seconds):
    return "{:02d}:{:02d}:{:02d}".format(
        seconds // 3600,         # hours
        (seconds % 3600) // 60,  # minutes
        seconds % 60             # seconds
    )


def val_or_error(callback):
    try:
        return callback()
    except Exception as ex:
        return ex.args[0]


# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    # check_time = check_time or datetime.utcnow().time()
    if check_time:
        check_time = check_time.strftime("%H:%M")
    else:
        check_time = datetime.now().time().strftime("%H:%M")
    # check_time = check_time or datetime.now().time().strftime("%H:%M")

    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def wait_between(rand_min=0.0, rand_max=5.0):
    rand = uniform(rand_min, rand_max)
    sleep(rand)


def get_full_hash_from_now():
    now = datetime.now()
    sha3_hash = hashlib.sha3_384()
    sha3_hash.update(now.utcnow().__str__().encode())
    return sha3_hash.hexdigest().upper()


def get_sub_hash_from_now(last_chars_count=10):
    return get_full_hash_from_now()[-last_chars_count:].upper()


def get_sub_hash_from_now_by_level(obfuscation_level=10):
    if obfuscation_level <= 0:
        return ''
    elif obfuscation_level > 10:
        return get_full_hash_from_now()
    else:
        last_chars_count = obfuscation_level / 10 * len(get_full_hash_from_now())
        return get_sub_hash_from_now(last_chars_count=int(last_chars_count))
