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

# OUTPUT list of i'm following:
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

# OUTPUT list of random users:
def get_random_users(following_list):
    res = sesh.get("https://api.github.com/users")
    linkArray = requests.utils.parse_header_links(res.headers['Link'].rstrip('>').replace('>,<', ',<'))
    url = linkArray[1]['url']
    #lastPage = url.split('=')[-1]
    #new_users = []
    try:
        f = open("last_page.txt", "r")
        last_page=int(f.read())
        f.close()
    except:
        last_page=1
    pages=30
    print('This may take a while... there are '+str(pages)+' pages to go through.')
    
    new_users = []
    try:
        with open("new_users_list.txt") as file_in:
            for line in file_in:
                new_users.append(line.replace('\n',''))
    except:
        pass

    fn=open("new_users_list.txt", "a")
    n_users=0
    for i in range(last_page,last_page+pages):
        res = sesh.get("https://api.github.com/users?since=" + str(i)).json()
        for user in res:
            if user['login'] not in following_list and user['login'] not in new_users:
                new_users.append(user['login'])
                print("Finding "+user['login'])
                fn.write(user['login']+"\n")
                n_users+=1
            else:
                pass
        #print(user['login'])
    f = open("last_page.txt", "w+")
    f.write(str(last_page+pages))
    f.close()
    fn.close()
    #print(n_users)
    print("Finding "+str(n_users)+" user")
    return new_users

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

following_list=following(args)
new_users_list=get_random_users(following_list)
#following_new(followers_list)