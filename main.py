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

# OUTPUT list of followers:
def followers(args):
    target = args.username
    res = sesh.get("https://api.github.com/users/" + target + "/followers")
    linkArray = requests.utils.parse_header_links(res.headers['Link'].rstrip('>').replace('>,<', ',<'))
    url = linkArray[1]['url']
    lastPage = url.split('=')[-1]
    followers = []
    print('Grabbing '+target+' Followers\nThis may take a while... there are '+str(lastPage)+' pages to go through.')
    x=0
    for i in range(1,int(lastPage)+1):
        res = sesh.get('https://api.github.com/users/' + target + "/followers?page=" + str(i)).json()
        for user in res:
            followers.append(user['login'])
            make_README(user['login'],user['avatar_url'])
    print("Total Followers: "+str(len(followers)))
    return followers

# OUTPUT list of following:
def following(args):
    target = args.username
    res = sesh.get("https://api.github.com/users/" + target + "/following")
    linkArray = requests.utils.parse_header_links(res.headers['Link'].rstrip('>').replace('>,<', ',<'))
    url = linkArray[1]['url']
    lastPage = url.split('=')[-1]
    following = []
    print('Grabbing '+target+' Following\nThis may take a while... there are '+str(lastPage)+' pages to go through.')
    x=0
    for i in range(1,int(lastPage)+1):
        res = sesh.get('https://api.github.com/users/' + target + "/following?page=" + str(i)).json()
        for user in res:
            following.append(user['login'])
    print("Total Following: "+str(len(following)))
    return following

def following_my_followers(followers_list,following_list):
    print("Starting to Follow Users...")
    for i in range(len(followers_list)):
        if not followers_list[i] in following_list:
            time.sleep(2)
            res = sesh.put('https://api.github.com/user/following/' + followers_list[i])
            if res.status_code != 204:
                print("Rate-limited, please wait until it finish!")
                time.sleep(60)
            else:
                print("Start Following : "+ followers_list[i])

def unfollowing_my_unfollowers(followers_list,following_list):
    print("Starting to Unfollowing Users...")
    for i in range(len(following_list)):
        if not following_list[i] in followers_list:
            time.sleep(2)
            res = sesh.delete('https://api.github.com/user/following/' + following_list[i])
            if res.status_code != 204:
                print("Rate-limited, please wait until it finish!")
                time.sleep(60)
            else:
                print("Unfollowing : "+ following_list[i])

def make_README(id="",url="",clear=False):
    if clear==False:
        f = open('README.md','a')
        img=f'<a href="https://github.com/{id}"><img src="{url}" alt="{id}" style="height:50px;width:50px;"/></a>'
        f.write(img)
        f.close
    else:
        f = open('README.md','w+')
        now = datetime.now()
        f.write("<h1>My Followers</h1>\n")
        f.write(f'<br><h4>last update at : {now.strftime("%d/%m/%Y %H:%M:%S")}</h4>\n')
        f.close
    os.remove("index.html")
    shutil.copy2('README.md','index.html')


make_README(clear=True)
followers_list=followers(args)
following_list=following(args)
following_my_followers(followers_list,following_list)
unfollowing_my_unfollowers(followers_list,following_list)
#}END.