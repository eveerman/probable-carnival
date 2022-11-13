import sys
from os import path
import argparse

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

def checkFile(secdef_file):
    exit = False
    input_file_exists = path.exists(secdef_file)
    if not input_file_exists:
        print("Input File does not exists, attempt download ...")

        exit = True
    if exit == True:
        sys.exit()

def main():
    secdef_file = getArgs()
    checkFile(secdef_file)
    print("FINISHED")

if __name__ == '__main__':
    main()
