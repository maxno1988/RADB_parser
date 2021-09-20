import os
import re

fnm = open('fnm_ready_prefixes.sh', 'w')
radb = open('whois_ready_prefixes.txt', 'w')
fnm.write('#!/bin/bash' + '\n')
text = open('prefix-list.txt', 'r').readlines()
n = 0
def prefix_divider(ip, n):
    mask = int(ip.split("/")[-1])
    oct1 = ip.split(".")[0]
    oct2 = ip.split(".")[1]
    oct3 = ip.split(".")[2]
    if (mask >= 16) & (mask < 24):
        increment = 2**(24 - mask)
        for i in range(increment):
            fnm.write('sudo fcli set main networks_list' + ' ' + oct1 + '.' + oct2 + '.' + str((int(oct3) + i)) + '.0/24' + '\n')
            radb.write(oct1 + '.' + oct2 + '.' + str((int(oct3) + i)) + '.0/24' + '\n')
            n = n + 1
            if n > 50:
                fnm.write('sudo fcli commit' + '\n')
                fnm.write('sleep 2' + '\n')
                n = 0
    if (mask == 24):
        fnm.write('sudo fcli set main networks_list' + ' ' + ip + '\n')
        radb.write(ip + '\n')
        n = n + 1
        if n > 50:
            fnm.write('sudo fcli commit' + '\n')
            fnm.write('sleep 2' + '\n')
            n = 0
    elif (mask < 16):
        increment = 2**(16 - mask)
        for i in range(increment):
            for j in range (256):
                fnm.write('sudo fcli set main networks_list' + ' ' + oct1 + '.' + str(int(oct2) + i) + '.' + str((int(oct3) + j)) + '.0/24' + '\n')
                radb.write(oct1 + '.' + str(int(oct2) + i) + '.' + str((int(oct3) + j)) + '.0/24' + '\n')
                n = n + 1
                if n > 50:
                    fnm.write('sudo fcli commit' + '\n')
                    fnm.write('sleep 2' + '\n')
                    n = 0
    return n
for count, line in enumerate(text):
    n = n + 1
    n = prefix_divider(line.strip(), n)
    if n > 50:
        fnm.write('sudo fcli commit' + '\n')
        fnm.write('sleep 2' + '\n')
        n = 0
fnm.write('sudo fcli commit' + '\n')
fnm.close()
radb.close()
