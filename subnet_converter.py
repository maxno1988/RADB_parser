import os
import re


radb = open('whois_ready_prefixes.txt', 'w')
text = open('prefix-list.txt', 'r').readlines()
def prefix_divider(ip):
    mask = int(ip.split("/")[-1])
    oct1 = ip.split(".")[0]
    oct2 = ip.split(".")[1]
    oct3 = ip.split(".")[2]
    if (mask >= 16) & (mask < 24):
        increment = 2**(24 - mask)
        for i in range(increment):
            radb.write(oct1 + '.' + oct2 + '.' + str((int(oct3) + i)) + '.0/24' + '\n')
    if (mask == 24):
        radb.write(ip + '\n')
    elif (mask < 16):
        increment = 2**(16 - mask)
        for i in range(increment):
            for j in range (256):
                radb.write(oct1 + '.' + str(int(oct2) + i) + '.' + str((int(oct3) + j)) + '.0/24' + '\n')
for count, line in enumerate(text):
    prefix_divider(line.strip())
radb.close()
