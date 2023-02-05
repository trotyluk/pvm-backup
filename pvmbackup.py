#!python3
# program to backup virtual machines into NAS storage
# program use external 7z program to make backups and scp command to transport
# to use scp the NAS ssh public key should be in the system namespace
import fnmatch
import argparse
import os
import re
import sys

def checkIP(Ip):
    # ip regular expression
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        
    # pass the regular expression
    # and the string in search() method
    if(re.search(regex, Ip)):
        return True 
    else:
        return False
# list of virtual machines
def getting_args():
    # argument analysis
    # Python program to demonstrate
    # command line arguments
    # Initialize parser
    # //TODO - Ip validation
    del_flag =''
    parser = argparse.ArgumentParser()
    # Adding optional argument
    parser.add_argument("-d", "--dirpath")
    parser.add_argument("-p", "--port", type=int)
    parser.add_argument("-i", "--ip", type=str)
    parser.add_argument("-e", "--erase", action="store_true")
    # Read arguments from command line
    args = parser.parse_args()
    if args.port:
        port= int(args.port)
        
    else:
        port=22
    if args.dirpath:
        dirpath=args.dirpath
    else:
        dirpath='.'
    if args.ip:
        ip = args.ip
        if checkIP(args.ip):
            error = False
            
        else:
            error=True
            
        
    else:
        ip = '192.168.18.28'
    erase = False
    if args.erase:
        erase = True
    
    return dirpath, port, ip, erase, error

try:
    zdirpath, zport, zip, zerase,error  = getting_args()
    if error:
        raise ValueError(f"invalid IP address {zip}")
        exit
except ValueError as e:
    print(e)
    sys.exit('max address = 255.255.255.255')
    
print(f"zdirpath = {zdirpath}\nzport = {zport}\nzip = {zip}\nzerase = {zerase}")

pvmlist= fnmatch.filter(os.listdir('.'), '*.pvm')
print(pvmlist)

    



