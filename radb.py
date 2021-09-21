import os
import time
import re
from ipwhois.net import Net
from ipwhois.asn import IPASN
from progress.bar import Bar
#Builds a list of ASNs
def as_set_stormwall_get():
    stream = os.popen("whois -h whois.radb.net AS-STORMWALL-SET | grep members: | awk '{print $2}'")
    result = stream.readlines()
    AS_LIST = []
    AS_SET_LIST = []
    bar = Bar('AS-SET Processing', max = len(result))
    for i in result:
        bar.next()
        AS = i.split('\n')[0]
        x = re.match("AS[0-9]+", AS)
        if x is None:
            stream2 = os.popen("whois -h whois.radb.net " + AS + " | grep members: | awk '{print $2}'")
            time.sleep(0.5)
            result2 = stream2.readlines()
            for s in result2:
                AS = s.split('\n')[0]
                AS_SET_LIST.append(AS)
        else:
            AS_LIST.append(AS)
    bar.finish()
    AS_LIST.extend(AS_SET_LIST)
    return AS_LIST



def prefix_check(AS_LIST):
    with open('whois_ready_prefixes.txt', 'r') as f:
        for i in f.readlines():
            try:
                net = Net(i.split('/')[0])
                obj = IPASN(net)
                result = obj.lookup()
            except ValueError:
                print("Prefix {} is not a correct format".format(i))
            AS = 'AS' + result['asn']
            time.sleep(1)    
            if AS in AS_LIST:
                print("Match for {} and {} is found".format(i.strip(), AS))
            else:
                print("No match for {}".format(i))

if "__name__ == __main__":
    AS_LIST = as_set_stormwall_get()
    prefix_check(AS_LIST)
