#!/usr/bin/python

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

URL = ("https://colwizlive.andover.edu/cgi-bin/wwiz.exe/wwiz.asp?" +
    "wwizmstr=WEB.STU.SCHED1.SUBR&stuid=%s&uid=0558956&uou=student")

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

def load_schedules(auth):
    s = requests.Session()
    s.mount('https://', SSLAdapter())
    for s_id in open('student.ids'):
        htmlrequest = s.get(URL % s_id, auth=auth)
        yield htmlrequest.text
