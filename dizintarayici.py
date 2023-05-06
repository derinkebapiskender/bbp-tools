import requests, concurrent.futures, threading, sys, signal
import time
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Counter(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.num = 0

    def increment(self, n=1):
        with self.lock:
            self.num += n

    def getValue(self):
        return self.num

def wait_threads():
    threads_running = True
    while threads_running:
        threads_running = False
        for future in results:
            if not future.done():
                threads_running = True
                break
        time.sleep(2)    

def sig_handler(signum, frame):
    for future in results:
        future.cancel()

    time.sleep(2)
    print(bcolors.WARNING+"\n\n [*] CTRL+C Received"+bcolors.ENDC)
    print(bcolors.OKGREEN+"\n [*] Waiting for threads to complete"+bcolors.ENDC)
    wait_threads()
    print(bcolors.OKGREEN+"\n [*] All Done!\n"+bcolors.ENDC)
    sys.exit(0)



    

def Action(uri,isUpper,filterResponse,method,kw):
    try:
        counter.increment()
        if int(isUpper) == 1:
            kw = kw[0].upper() + kw[1:]
        target = uri.replace('FUZZ',kw)
        
        r = requests.request(method.upper(),target,headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0"},allow_redirects=False,verify=False,timeout=7)

        if len(filterResponse) == 3:
            if r.status_code != 404 and r.status_code != int(filterResponse):
                if r.status_code == 303 or r.status_code == 301 or r.status_code == 302 or r.status_code == 307:
                    return {"url":str(r.url),"status_code":str(r.status_code),"content_length":str(len(r.content)),"location":str(r.headers["Location"])}
                else:
                    return {"url":str(r.url),"status_code":str(r.status_code),"content_length":str(len(r.content))}
        elif filterResponse == "":
            if r.status_code != 404:
                if r.status_code == 303 or r.status_code == 301 or r.status_code == 302 or r.status_code == 307:
                    return {"url":str(r.url),"status_code":str(r.status_code),"content_length":str(len(r.content)),"location":str(r.headers["Location"])}
                else:
                    return {"url":str(r.url),"status_code":str(r.status_code),"content_length":str(len(r.content))}
        else:
            return None
    except:
        return None

if __name__ == "__main__":
    global results
    signal.signal(signal.SIGINT, sig_handler)
    counter=Counter()

    method=input("\n [*] Request Method?(GET istersen pas gec): ")
    if str(method) == "":
        method="GET"
        
    wordlists_=input("\n [*] Choose your wordlist\n  [1] wordlists/medium.txt\n  [2] wordlists/raft-large-words.txt\n  [3] wordlists/big.txt\n\n [*] Hangisi: ")

    wl_loc="wordlists/medium.txt"
    if wordlists_ == 1 or wordlists_ == "1":
        wl_loc="wordlists/medium.txt"
    elif wordlists_ == 2 or wordlists_ == "2":
        wl_loc="wordlists/raft-large-words.txt"
    elif wordlists_ == 3 or wordlists_ == "3":
        wl_loc="wordlists/big.txt"
        
    wlist=open("/tmp/"+wl_loc,"r").read().splitlines()
    wordlist_size = 220546
    found_count = 0
    url=input("\n [*] Target URL [https://google.com/FUZZ] : ")
    if "FUZZ" not in url:
        print(bcolors.FAIL+f"\n [*] {url} not valid, use FUZZ kw to run this script\n"+bcolors.ENDC)
        sys.exit(0)
    elif "://" not in url:
        print(bcolors.FAIL+f"\n [*] {url} not valid url, like https://google.com/\n"+bcolors.ENDC)
        sys.exit(0)
        
    isUpper=input("\n [*] is first char uppper like getFuzz?[enter to pass / 1-0 ]: ")
    
    filterResponse=input("\n [*] Filter response code[enter to pass/[200,403,200]/500]: ")

    print("")
    if str(isUpper) == "":
        isUpper=0

    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        results = [executor.submit(Action, url, isUpper, filterResponse, method, kw) for kw in wlist]
        for future in concurrent.futures.as_completed(results):
            res = future.result()
            if res != None:
                found_count += 1
                status_code=res["status_code"]
                if status_code=="200":
                    status_code=bcolors.OKGREEN+status_code+bcolors.ENDC
                elif status_code == "403" or status_code == "401":
                    status_code=bcolors.FAIL+status_code+bcolors.ENDC
                    
    
                    
                url=bcolors.WARNING+res["url"]+bcolors.ENDC
                printable_cl=res["content_length"]+str((5-len(res["content_length"]))*" ")
                
                if "location" in res.keys():
                    status_code=bcolors.WARNING+status_code+bcolors.ENDC
                    loc = bcolors.OKBLUE+res["location"]+bcolors.ENDC
                    result_text = " ["+status_code+"]  - CL: "+printable_cl+"-  URL: "+url+" - Location: "+loc
                else:
                    result_text = " ["+status_code+"]  - CL: "+printable_cl+"-  URL: "+url
                print(result_text,end="\r\n")
            else:
                print(f" [x] {found_count} found of "+str(counter.getValue())+f"/{wordlist_size}",end="\r")
