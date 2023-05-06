import requests, os, subprocess
import json, sys

hedef = sys.argv[1]
print "\n [*] Hedef: %s " % str(hedef)

api_key="your_api_key"

def islem(hedef):
    try:
        r = requests.get("http://api.whoxy.com/?key="+api_key+"&reverse=whois&mode=micro&company="+str(hedef))
        print "\n [*] sending request"
        al = raw_input("\n\n [*] Kaydedilecek dosya ismi ( orn. Google, Tiktok) : ")
        fname = './reverse-whois-domains/'+al+'-domains.txt'
        hax = []
        kaynak = r.content
        c = json.loads(kaynak)
        result_count = len(c["search_result"])
 
        for i in range(result_count):
            domain = c["search_result"][i]["domain_name"]
            if domain not in hax:
                hax.append(domain)
            else:
                pass
        
        yaz = open(fname,'a')
        for h in hax:
            yaz.write(str(h)+"\n")
        print "\n [*] "+str(len(hax))+" Adet domain bulundu ve dosyaya yazdirildi\n"
        
    except:
        raise
    
islem(hedef)
print "\n\n[*] Finito\n"
