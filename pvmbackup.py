#!python3
# program to backup virtual machines into NAS storage
# program use external 7z program to make backups and scp command to transport
# to use scp the NAS ssh public key should be in the system namespace
import fnmatch
import argparse
import os
import sys
# list of virtual machines
def getting_args():
    # argument analysis
    # Python program to demonstrate
    # command line arguments
    # Initialize parser
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
        ip= args.ip
    else:
        ip = '192.168.18.28'
    erase = False
    if args.erase:
        erase = True
    
    return dirpath, port, ip, erase


zdirpath, zport, zip, zerase = getting_args()
print(f"zdirpath = {zdirpath}\nzport = {zport}\nzip = {zip}\nzerase = {zerase}")






pvmlist= fnmatch.filter(os.listdir('.'), '*.pvm')
print(pvmlist)

    



