import sys
from os import path
import argparse
import ftplib
import gzip 
import shutil

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('secdef_file',
                        default = 'secdef.dat',
                        help = 'name of or path to secdef file, default is ./secdef.dat',
                        type = str,
                        nargs = '?',)
    arguments = parser.parse_args()
    secdef_file = arguments.secdef_file
    return secdef_file

def retrieveSecdef():
    host = 'ftp.cmegroup.com'
    #secdef_path = "SBEFix/Production/secdef.dat.gz"
    filename = 'secdef.dat.gz'
    file = open(filename, 'wb')
    server = ftplib.FTP(host)
    server.login()
    #server.retrbinary('RETR {secdef_path}', file.write)
    server.retrbinary('RETR SBEFix/Production/secdef.dat.gz', file.write)
    print("File downloaded, unpacking ...")
    with gzip.open('secdef.dat.gz', 'rb') as unpack:
        with open('secdef.dat', 'wb') as unpacked:
            shutil.copyfileobj(unpack, unpacked)
    server.quit()
            
def checkFile(secdef_file):
    exit = False
    input_file_exists = path.exists(secdef_file)
    if not input_file_exists:
        print("Input File does not exists, attempt download ...")
        retrieveSecdef()
        input_file_exists = path.exists(secdef_file)
        if not input_file_exists:
            print("I've borked something :(")
            exit = True
    if exit == True:
        sys.exit()

def main():
    secdef_file = getArgs()
    checkFile(secdef_file)
    print("FINISHED")
    #with open(secdef_file) as file:
    #    first5 = [next(file) for x in range(5)]
    #print(first5)

if __name__ == '__main__':
    main()
