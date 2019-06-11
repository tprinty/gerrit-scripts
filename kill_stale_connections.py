#!/usr/bin/env python

from pygerrit2 import GerritRestAPI
from requests.auth import HTTPDigestAuth
from datetime import datetime, timedelta
import pprint
import json
import os

auth = HTTPDigestAuth('user', 'http-password-from-settings')
rest = GerritRestAPI(url='http://yourserver:8080', auth=auth)
tasks = rest.get("/config/server/tasks/")
pp = pprint.PrettyPrinter(indent=4)

for task in tasks:
    task["start_time"] = task["start_time"].split('.')[0]
    taskdate = datetime.strptime(task["start_time"], "%Y-%m-%d %H:%M:%S")
    if ( (datetime.now() > taskdate + timedelta(hours=4)) and (task["command"] != "Log File Compressor") and (task["command"] != "change cleanup runner") ):
        print "Killing: " + task["id"] + " " + task["start_time"] + " " + task["command"]
        os.system('ssh -p 29418 gerrit@yourserver kill '+ task["id"])

