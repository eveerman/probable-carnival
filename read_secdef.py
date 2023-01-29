import sys
from os import path
import argparse
import ftplib
import gzip 
import shutil
from datetime import datetime


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('secdef_file',
                        default = 'secdef.dat',
                        help = 'name of or path to secdef file, default is ./secdef.dat.gz',
                        type = str,
                        nargs = '?',)
    arguments = parser.parse_args()
    secdef_file = arguments.secdef_file
    return secdef_file

def retrieveSecdef():
    host = 'ftp.cmegroup.com'
    filename = "secdef.dat.gz"
    file = open(filename, 'wb')
    server = ftplib.FTP(host)
    try:
        server.login()
    except:
        print("Failed to open connection to {host}")
    server.retrbinary('RETR SBEFix/Production/secdef.dat.gz', file.write)
    server.close()
    server.quit()
    print("File downloaded, unpacking ...")
    with gzip.open(filename, 'rt') as secdef_data:
        secdef_data = secdef_data.read()
        with open('secdef.dat', 'w') as out:
            print(secdef_data, file=out)
    #return secdef_data
       
def checkFile(secdef_file):
    exit = False
    input_file_exists = path.exists(secdef_file)
    if not input_file_exists:
        print("Input File does not exist, attempt download ...")
        retrieveSecdef()
        input_file_exists = path.exists(secdef_file)
        if not input_file_exists:
            print("I've borked something :(")
            exit = True
    if exit == True:
        sys.exit()


def startParsing(secdef_file):
    ## intersting tags: 167, 462, 55, 200, 6937, 555
    ## hashmap?
    tags_map = {
        '167' : 'Security', #Security (all)
        '462' : 'UnderlyingProduct', #ProductComplex (all)
        '55' : 'Symbol', #names (all)
        '200' : 'MaturityMonthYear', #Expiration (all)
        '6937' : 'Asset', #Asset (all)
        '555' : 'NoLegs' #legs (spreads)
    }

    #with open(secdef_file) as file:
    #    first5 = [next(file) for x in range(5)]
    #print(first5)

    with open(secdef_file) as file:
        all_secdef = file.read()
    all_secdef = [l for l in all_secdef.split('\n') if l]
    #print(all_secdef[0].split('\x01'))
    #listy = []
    #count = 0

    #for ln in all_secdef:
    #    listy += '='.join(ln.strip('\x01').split('\x01')).split('=')
    #print(type(listy))
    #rint(listy[:10])
    
    data = {}
    i = 0
    for ln in all_secdef:
        item = '='.join(ln.strip('\x01').split('\x01')).split('=')
        oneln = iter(item)
        data[i] = dict((key,value) for key, value in zip(oneln, oneln) if key in tags_map.keys())
        i += 1
    print(item)
    #print(type(data))
    print(data[0])
    #total = len(data)
    #print(data)
    security = []
    products = []
    ge = []
    #print
    for item in data:
        security += {data[item]['167']}
        if 'FUT' in {data[item]['167']}:
            if '462' in data[item]:
                products.append(data[item]['462'])
            if 'GE' == data[item]['6937']:
                #print(data[item])
                if '555' not in data[item]:
                    #print(data[item])
                    appendge= {}
                    appendge["name"] = data[item]['55']
                    appendge["expiry"] = data[item]['200']
                    ge.append(appendge)
                    del appendge

    ## for future: learn to use pandas :/

    #print(security[:5])
    securities = []

    for x in security:
        if x not in securities:
            securities.append(x)
    for x in securities:
        print(x)
        print(security.count(x))

    list_products = set(products)
    #print(list(list_products))
    for x in set(products):
        print(x)
        print(products.count(x))

    #print(ge)
    ge.sort(key = lambda x: datetime.strptime(x['expiry'], '%Y%m'))
    for x in ge[:4]:
        print(f'{x}')

    #print(appendge)
    #    print(products.count(x))
    #keys = {}
    #values = {}
    #for key, nested in data.iteritems():
    #    for 
    #values_per_key = {}
    #for item in data:
    #    for k, v in item.items():
    #        values_per_key.setdefault(k, set()).add(v)
    #counts = {k: len(v) for k, v in values_per_key.items()}
    #counts
    #print(data)



def main():
    secdef_file = getArgs()
    checkFile(secdef_file)
    #print("FINISHED")
    startParsing(secdef_file)
    
    print("COMPLETE")

if __name__ == '__main__':
    main()
