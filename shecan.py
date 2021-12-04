#!/bin/python3

import os
import sys
import requests

resolv_conf_content = """
# writed by shecan-cli

nameserver 185.51.200.2
nameserver 178.22.122.100

"""

def check_root():
    if os.geteuid() != 0:
        print("run as root")
        exit(-1)

def disable():
    check_root()
    os.system("cat /etc/resolv.conf.tmp > /etc/resolv.conf")
    os.system("rm /etc/resolv.conf.tmp")
    print("shcan disabled")

def enable():
    check_root()
    os.system('cp /etc/resolv.conf /etc/resolv.conf.tmp')
    file = open("/etc/resolv.conf","w")
    file.write(resolv_conf_content)
    file.close()
    print("shcan enabled")

# TODO
# def keep_enable():
#     while True:
#         enable()
#         sleep(10000)

def bool_to_status(bool_value):
    if bool_value:
        return "OK"
    else:
        return "Err"


def local_status():
    file = open("/etc/resolv.conf","r")
    content = file.read()
    file.close()
    if content == resolv_conf_content:
        return True
    else:
        return False

def ping_status():
    try:
        r = requests.get("http://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

def remote_status():
    return True

def status():
    print("local\t\tping\t\tisShecanized")
    print(bool_to_status(local_status())+"\t\t",end="")
    print(bool_to_status(ping_status())+"\t\t",end="")
    print(bool_to_status(remote_status())+"\t\t")

def live_status():
    pass

def show_help():
    print("┌────────────────────────────────────────────────────────┐");
    print("│                        shecan-cli                      │");
    print("│ > https://github.com/ali77gh/shecan-cli                │");
    print("│                                                        │");
    print("├────────────────────────────┬───────────────────────────┤");
    print("│ > how to use:              │                           │");
    print("│   shecan-cli help          │ show this beautiful msg   │");
    print("│   shecan-cli status        │ show status (local&remote)│");
    print("│   shecan-cli enable        │ enables shcan DNS         │");
    print("│   shecan-cli disable       │ load your old DNS config  │");
    print("│   shecan-cli live_status   │ run status in loop        │");
    print("│                            │                           │");
    print("└────────────────────────────┴───────────────────────────┘");

def main_switch(argv):
    if argv == "enable":
        enable()
    elif argv == "disable":
        disable()
    elif argv == "status":
        status()
    elif argv == "live_status":
        live_status()
    elif argv == "help":
        show_help()
    else:
        print("unkown param: "+ argv)
        show_help()

def main():
    if len(sys.argv) != 2:
        show_help()
    else:
        main_switch(sys.argv[1])

main()