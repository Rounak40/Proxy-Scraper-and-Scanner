# import modules
import requests
import json
from bs4 import BeautifulSoup
import re
from threading import Thread

global good_list
good_list = []

def get_links(proxy_type=None):
    if proxy_type == "http":
         data = open("site urls.txt").readlines()[0]
    elif proxy_type == "https":
         data = open("site urls.txt").readlines()[1]
    elif proxy_type == "socks4":
         data = open("site urls.txt").readlines()[2]
    elif proxy_type == "socks5":
         data = open("site urls.txt").readlines()[3]
    else:
         data = ""
    return [i.strip() for i in data.split(",") if len(i) > 10]

def parse_proxies_from_html_response(response_data):
    data = re.findall(r'[\w\.-]+:[\w\.-]+', response_data, re.MULTILINE)
    proxies = []
    for i in data:
        if "." in i:
            if i.split(":")[1].isdigit():
                proxies.append(i+"\n")
    return proxies

def scrap_proxies(proxy_type=None):
    requests_links = get_links(proxy_type)
    print("Scraping proxies....")
    response_data = """
"""
    for i in requests_links:
        try:
            res = requests.get(i,timeout=10).text
        except:
            res = ""
        response_data += res
    proxy_list = parse_proxies_from_html_response(response_data)
    
    with open(proxy_type.upper()+"-proxies.txt","w+") as file:
        file.writelines(proxy_list)
    print("Saved Successfully!")
    ask_input()

def check_proxy_by_url(proxy,url,timeout):
    global good_list
    p = dict(http=proxy, https=proxy)
    try:
        r = requests.get(url, proxies=p, timeout=timeout)
        if r.status_code == 200:
            good_list.append(proxy+"\n")
    except Exception as e:
        pass

def main(proxy_type,proxy_list):
    global good_list
    proxy_list2 = [proxy_type.lower()+"://"+i.strip() for i in proxy_list]
    thread_list = []
    lists = proxy_list2
    print("Scanning",len(lists),proxy_type.upper(),"proxies...")
    for l in lists:
        t = Thread(target=check_proxy_by_url, args=[l,"http://ipinfo.io/json",10])
        t.start()
        thread_list.append(t)
    for x in thread_list:
        x.join()
    print('Proxies Scanned .')
    with open(proxy_type.upper()+"-working-proxies.txt","w+") as file:
        file.writelines(good_list)
    ask_input()
        
def ask_proxy_type():
    proxy_type = input("Which type of proxy you want to Scrape/Scan?\n1.HTTP\n2.HTTPS\n3.SOCKS4\n4.SOCKS5\n5.Back\n==>")
    if str(proxy_type) == "1":
        return "http"
    elif str(proxy_type) == "2":
        return "https"
    elif str(proxy_type) == "3":
        return "socks4"
    elif str(proxy_type) == "4":
        return "socks5"
    elif str(proxy_type) == "5":
        ask_input()
    else:
        print("Wrong input try again!")
        ask_proxy_type()
 
def ask_input():
    user_input = input("What you want to do? (Enter 1 or 2)\n1.Scrape Proxies.\n2.Scan Proxies \n==>")
    if str(user_input) == "1":
        proxy_type = ask_proxy_type()
        scrap_proxies(proxy_type)
    elif str(user_input) == "2":
        proxy_type = ask_proxy_type()
        file = input("File Name: ")
        main(proxy_type,open(file).readlines())
    else:
        print("Wrong input try again!")
        ask_input()

if __name__ == "__main__":
    print("Welcome in Proxy Scrapper + Scanner.")
    ask_input()
