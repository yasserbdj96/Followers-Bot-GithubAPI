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

# OUTPUT list of my followers:
def followers(args):
    target = args.username
    res = sesh.get("https://api.github.com/users/" + target + "/followers")
    linkArray = requests.utils.parse_header_links(res.headers['Link'].rstrip('>').replace('>,<', ',<'))
    url = linkArray[1]['url']
    lastPage = url.split('=')[-1]
    followers = []
    followers_avatar = []
    print('Grabbing '+target+' Followers\nThis may take a while... there are '+str(lastPage)+' pages to go through.')
    x=0
    for i in range(1,int(lastPage)+1):
        res = sesh.get('https://api.github.com/users/' + target + "/followers?page=" + str(i)).json()
        for user in res:
            followers.append([user['login'],user['avatar_url']])
            #make_README(user['login'],user['avatar_url'])
    print("Total Followers: "+str(len(followers)))
    return followers

followers_info=followers(args)

f = open('README.md','w+')
now = datetime.now()
f.write("<p>This bot is programmed on GithubAPI in order to increase the number of followers on github, it follows about 30 users every 60 minutes, or about 720 every 24 hours, and follows those who follow me every 24 hours, and unfollows members who have been followed and did not follow me every week (Excessive use of this bot may result in a ban).</p>")
f.write("\n\n[![Join the chat at https://gitter.im/yasserbdj96/Followers-Bot-GithubAPI](https://badges.gitter.im/yasserbdj96/Followers-Bot-GithubAPI.svg)](https://gitter.im/yasserbdj96/Followers-Bot-GithubAPI?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n\n")
f.write("<h1>My Followers:</h1><br>\n")
for i in range(len(followers_info)):
    f.write(f'<a href="https://github.com/{followers_info[i][0]}"><img src="{followers_info[i][1]}" alt="{followers_info[i][0]}" style="height:50px;width:50px;"/></a>\n')
f.write(f'<br><h4>last update at : {now.strftime("%d/%m/%Y %H:%M:%S")} (UTC)</h4><br>')
f.close

import json

with open("Dataset.json", "w") as f:
    json.dump(followers_info, f)
"""
try:
    os.remove("index.html")
except:
    pass
shutil.copy2('README.md','index.html')
#print(followers_list)
#print(following_list)"""