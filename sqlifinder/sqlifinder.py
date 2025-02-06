import requests
import re
import argparse
import os
import sys
import time
import string

from huepy import *
from core import requester
from core import extractor
from core import crawler
from urllib.parse import unquote
from tqdm import tqdm 

start_time = time.time()

def clear():
    if 'linux' in sys.platform:
        os.system('clear')
    elif 'darwin' in sys.platform:
        os.system('clear')
    else:
        os.system('cls')

def banner():
    ban = '''
            ___ ____         __       
  ___ ___ _/ (_) _(_)__  ___/ /__ ____  
 (_-</ _ `/ / / _/ / _ \/ _  / -_) __/  
/___/\_, /_/_/_//_/_//_/\_,_/\__/_/   
      /_/        ~ by @americo        v1.0 
      '''
    print(green(ban))

def concatenate_list_data(list, result):
    for element in list:
        result = result + "\n" + str(element)
    return result

def main():
    parser = argparse.ArgumentParser(description='xssfinder - a xss scanner tool')
    parser.add_argument('-d', '--domain', help = 'Domain name of the target [ex. example.com]', required=True)
    parser.add_argument('-s', '--subs', help = 'Set false or true [ex: --subs False]', default=False)
    args = parser.parse_args()

    # Verbose output to confirm input arguments
    print(f"\n{blue('[INF]')} Starting scan for domain: {args.domain}")
    if args.subs:
        print(f"{blue('[INF]')} Scanning subdomains: Enabled")
    else:
        print(f"{blue('[INF]')} Scanning subdomains: Disabled")
    
    if args.subs == True:
        url = f"http://web.archive.org/cdx/search/cdx?url=*.{args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    else:
        url = f"http://web.archive.org/cdx/search/cdx?url={args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"

    clear()
    banner()

    print(f"{blue('[INF]')} Connecting to the Wayback Machine to fetch URLs...")
    response = requester.connector(url)
    
    print(f"{blue('[INF]')} Starting web crawling on {args.domain}...")
    crawled_urls = crawler.spider(f"http://{args.domain}", 10)
    response = concatenate_list_data(crawled_urls, response)
    
    if response == False:
        print(f"{red('[ERR]')} No URLs found to scan.")
        return
    
    response = unquote(response)

    print(f"\n{blue('[INF]')} Scanning SQL injection vulnerabilities for {args.domain}...")
    
    exclude = ['woff', 'js', 'ttf', 'otf', 'eot', 'svg', 'png', 'jpg']
    final_uris = extractor.param_extract(response , "high", exclude, "")

    file = open('payloads.txt', 'r')
    payloads = file.read().splitlines()

    vulnerable_urls = []

    # Verbose message for scanning payloads
    print(f"{blue('[INF]')} Loaded {len(payloads)} payloads from payloads.txt\n")

    for uri in final_uris:
        for payload in payloads:
            final_url = uri + payload
            
            try:
                print(f"{blue('[INF]')} Testing {final_url} for SQL injection...")
                req = requests.get("{}".format(final_url))
                res = req.text
                if 'SQL' in res or 'sql' in res or 'Sql' in res:
                    print(f"{green('[sql-injection]')} Vulnerable URL: {final_url}")
                    vulnerable_urls.append(final_url)
                    break  # Stop once the first vulnerability is found for this URL
            except requests.exceptions.RequestException as e:
                print(f"{red('[ERR]')} Error accessing {final_url}: {e}")
                pass

    print(f"\n{blue('[INF]')} SQL Injection scan complete.")
    print(f"{blue('[INF]')} Found {len(vulnerable_urls)} vulnerable URL(s).")

if __name__ == "__main__":
    clear()
    banner()
    main()

