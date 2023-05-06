import requests, json, sys
from urlparse import urlparse
import tldextract

is_only_domain = input("\n [*] Yalnizca domainleri mi alican? [0-1]: ")
org_veya_domain=raw_input("\n [1] Organization\n [2] Domain\n  [?] Hangisi: ")

if str(org_veya_domain) == "1" or str(org_veya_domain) == "2":
    pass
else:
    print "\n [ * ] HATALI SECIM [ * ]"
    sys.exit(0)
    
hedef=raw_input("\n [*] Hedef: ")

if org_veya_domain ==1:
    param = "O"
else:
    param = "q"

uri = "https://crt.sh/?"
user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0"
domains=[]

def islem(param,hedef,ua,is_only_domain):
    global domains
    try:
        parameters = param+"="+hedef+"&output=json"
        r = requests.get(uri+parameters,headers={"User-Agent":ua})
        if r.status_code == 200:
            pass
        else:
            print "\n [*] kaynak cekme hatali, status_code %s - length %s " % (str(r.status_code),str(len(r.content)))
        kaynak = json.loads(r.content)
        say = len(kaynak)
        for i in range(say):
            cn = kaynak[i]['common_name']
            cn = cn.replace("*.","")
            if is_only_domain == 1:
                #domain = '.'.join(cn.split('.')[-2:])
                domain_name = tldextract.extract(cn)
                domain = domain_name.domain + "." + domain_name.suffix
                if domain not in domains:
                    domains.append(domain)
                else:
                    pass
            else:
                if cn not in domains:
                    if "crt.sh" in cn or "digicert" in cn:
                        pass
                    else:
                        domains.append(cn)
                else:
                    pass
                
        d_l = len(domains)
        print "\n [*] %s Adet domain bulundu " % str(d_l)
            
    except Exception as err:
        print "\n [ HATA VAR ] -- %s\n" % str(err)

def yazdir():
    global domains
    hedef_d = hedef.replace(".","")
    fname='/tmp/crt-sh-tarama-'+str(hedef_d)+'.txt'
    fname = fname.replace(" ","-")
    hedef_dosya = open(fname,'a')

    for d in domains:
        hedef_dosya.write(str(d)+str("\n"))

    print "\n [*] Hedef: file://%s" % str(fname)
    print "\n\n [**] Biter [**]\n"

islem(param,hedef,user_agent,is_only_domain)
yazdir()
