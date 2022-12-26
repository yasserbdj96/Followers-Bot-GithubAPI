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

# OUTPUT list of random users:
def following():
    res = sesh.get("https://api.github.com/users")
    linkArray = requests.utils.parse_header_links(res.headers['Link'].rstrip('>').replace('>,<', ',<'))
    url = linkArray[1]['url']
    #lastPage = url.split('=')[-1]
    following = []
    f = open("last_page.txt", "r")
    try:
        last_page=int(f.read())
    except:
        last_page=1
    print(last_page)
    pages=1
    print('This may take a while... there are '+str(pages)+' pages to go through.')
    
    x=0
    n_users=0
    #for i in range(last_page,last_page+pages):
    res = sesh.get("https://api.github.com/users?page=" + str(last_page)).json()
    for user in res:
        following.append(user['login'])
        n_users+=1
            #print(user['login'])
    f = open("last_page.txt", "w+")
    f.write(str(last_page+pages))
    print(n_users)
    print("Finding "+str(n_users)+" user")
    return following

def following_new(followers_list):
    print("Starting to Follow Users...")
    for i in range(len(followers_list)):
        time.sleep(2)
        res = sesh.put('https://api.github.com/user/following/' + followers_list[i])
        if res.status_code != 204:
            print("Rate-limited, please wait until it finish!")
            time.sleep(60)
        else:
            print("Start Following : "+ followers_list[i])

followers_list=following()
following_new(followers_list)
