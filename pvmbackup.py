#!python3
# program to backup virtual machines into NAS storage
# program use external 7z program to make backups and scp command to transport
# to use scp the NAS ssh public key should be in the system namespace
import fnmatch
import argparse
import os
import re
import sys
import shutil
import platform
import socket

# check operating system
def check_os():
    my_system = platform.uname()
    system = my_system.system
    node = my_system.node
    release = my_system.release
    version = my_system.version
    machine = my_system.machine
    processor = my_system.processor
    config = [system,node,release,version,machine,processor]
    # return configuration in the list format
    # [system,node,release,version,machine,processor]
    return config
    
# check if 7z exists
def check7z(osid):
    if osid == 'Windows':
        cmd = '7z.exe'
    else:
        cmd = '7z'
    path7z = shutil.which(cmd)
    return path7z

# check if port is open to connect by ssh
def check_port(ip,port):
    #checkin if port is open on IP address
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        s.settimeout(None)
        result=True
        s.close()
    except socket.error:
        result=False
    return result

#//TODO create send archive
#//TODO create make log
#//TODO create remove archives
#//TODO create check archive
# achive creation
def create_archve(archname):
    #pvmlist= fnmatch.filter(os.listdir('.'), '*pvm')
    create7z = '7z a "'+ archname +'.7z" "'+ archname + '"'
    # print(f'Creating {archname}.7z')
    os.system(create7z)  
    
# IP validation
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
    # Initialize parser
    parser = argparse.ArgumentParser()
    # Adding optional argument
    # addind path to scan
    parser.add_argument("-d", "--dirpath")
    # adding port
    parser.add_argument("-p", "--port", type=int)
    # adding IP address
    parser.add_argument("-i", "--ip", type=str)
    # adding erase flag -- erase local backups after transfer
    parser.add_argument("-e", "--erase", action="store_true")
    # adding send flag -- transfer backup to specified location
    parser.add_argument("-s", "--send", action="store_true")
    # adding file flag -- make backup single file
    parser.add_argument("-f", "--filename")
    # adding vmware flag to achive wmware vm
    parser.add_argument("-v", "--vmware", action="store_true")
    
    
    # Read arguments from command line
    args = parser.parse_args()
    send=False
    if args.port:
        port= int(args.port)
    else:
        port=22
    if args.dirpath:
        dirpath=args.dirpath
    else:
        dirpath='#'
    if args.send:
        send = True
        
    if args.ip:
        ip = args.ip
        if checkIP(args.ip):
            error = False
        else:
            error=True
            ip='None'
    else:
        ip='None'
        send = False
        error=False
    erase = False
    if args.erase:
        erase = True
    file = False
    if args.filename:
        file = args.filename
    else:
        file = "#"
    if args.vmware:
        vmware_s = True
    else:
        vmware_s = False
    return dirpath, port, ip, erase, send, file, vmware_s, error
#//TODO correct vm_dir_validation check directory extention accordint to vm_selector
def vm_dir_validation(cwd,filename,vm_selector):
    if filename != "#":
        
        full_path = os.path.join(cwd,filename)
        print(full_path)
        if (os.path.exists(full_path)):
            if (os.path.isdir(full_path)):
                #//TODO change test according to vm_selector
                if vm_selector == "pvm":
                    sel_name = "config.pvs"
                else:
                    sel_name = filename+"vmx"
                if (os.path.exists(os.path.join(full_path,sel_name))):
                    print(f"{sel_name} already exists")
                else:
                    print(f"{sel_name} not exist")
            # check if *hdd exists in the *pvm directory   
    else:
        print("no file")
    
    

try:
    zdirpath, zport, zip, zerase, zsend, zfile, zvmware, error  = getting_args()
    if error:
        raise ValueError(f"invalid IP address {zip}")
        exit
except ValueError as e:
    print(e)
    sys.exit('max address = 255.255.255.255')
# selector parallels/vmware    
if zvmware:
    vm_selector = "vmware" 
else:
    vm_selector = "pvm"

start_dir = os.getcwd()
print(f"zdirpath = {zdirpath}\nzport = {zport}\nzip = {zip}\nzerase = {zerase}\nzsend = {zsend}\nzfile = {zfile}")
print(f"zvmware = {zvmware}\nerror = {error}")
if zdirpath != "#" and zfile == "#":
    print(f"Compress all vm directories in {zdirpath} directory")
if zdirpath == "#" and zfile != "#":
    print(f"compress {zfile} directory")
if zdirpath == "#" and zfile == "#":
    zdirpath = '.'
    print("compress all vm directories in current directory")

    

#pvmlist= fnmatch.filter(os.listdir('.'), vm_ext)

# print(f"virtual machnes directory list:\n{pvmlist}")
print(f"Operating system: {check_os()[0]}")

print(f"Archiver path: {check7z(check_os()[0])}")
port=zport
ip="185.20.54.8"
if (check_port(ip,port)):
    print(f"Port {port} is open on {ip}")
else:
    print(f"Port {port} is closed on {ip}")

print(start_dir)
vm_dir_validation(start_dir, zfile, vm_selector)

# //TODO - if zfile True dirpath have one directory to archive
# //TODO - if zfile False dirpath have directory to archive all pvm directories




