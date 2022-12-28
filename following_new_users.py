#!/usr/bin/env python
# coding:utf-8
#   |                                                          |
# --+----------------------------------------------------------+--
#   |   Code by : yasserbdj96                                  |
#   |   Email   : yasser.bdj96@gmail.com                       |
#   |   Github  : https://github.com/yasserbdj96               |
#   |   BTC     : bc1q2dks8w8uurca5xmfwv4jwl7upehyjjakr3xga9   |
# --+----------------------------------------------------------+--  
#   |        all posts #yasserbdj96 ,all views my own.         |
# --+----------------------------------------------------------+--
#   |                                                          |

#START{
# IMPORT
import requests
import argparse
from base64 import b64encode
import time
import shutil
from hexor import *
import os
from datetime import datetime

# INPUT ARG
ap = argparse.ArgumentParser()
ap.add_argument('-t', '--token', required=True)
ap.add_argument('-m', '--username', required=True)
args = ap.parse_args()

p1=hexor(False,"hex")

# RESPONE AUTH
HEADERS = {"Authorization": "Basic " + b64encode(str(args.username + ":" + args.token).encode('utf-8')).decode('utf-8')}
res = requests.get("https://api.github.com/user", headers=HEADERS)
if(res.status_code != 200):
    p1.c("Failure to Authenticate! Please check PersonalAccessToken and Username!","#ff0000")
    exit(1)
else:
    p1.c("Authentication Succeeded!","#22a701")
	
# SESSION HEADER
sesh = requests.session()
sesh.headers.update(HEADERS)

def following_new(new_users):
    new_list=new_users
    print("Starting to Follow Users...")
    for i in range(len(new_users)):
        time.sleep(2)
        res = sesh.put('https://api.github.com/user/following/' + new_users[i])
        if res.status_code != 204:
            print("Rate-limited, please wait until it finish!")
            time.sleep(60)
        else:
            print("Start Following : "+ new_users[i])
            new_list.remove(new_users[i])
    f = open("new_users_list.txt", "w+")
    for i in range(len(new_list)):
        f.write(new_list[i]+"\n")
    f.close()
new_users = []
try:
    with open("new_users_list.txt") as file_in:
        for line in file_in:
            new_users.append(line.replace('\n',''))
            following_new(new_users)
except:
    pass