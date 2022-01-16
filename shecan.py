#!/usr/bin/env python3

import os
import sys
import requests
import platform
platform = platform.system()
from time import sleep

# global configs
ping_check_url =   "https://google.com"
shecan_check_url = "https://check.shecan.ir:8443" # provided by sniffing shecan.ir xhr request :)
shecan_dns = ["185.51.200.2","178.22.122.100"]

# linux configs
dns_file = "/etc/resolv.conf"
dns_file_bak = "/etc/resolv.conf.shecan.bak"

# OS X configs
interface = "Wi-Fi"
user = os.popen("whoami").read()
dns_file_bak_mac = f"/User/{user}/.shecan-cli"

def check_root():
   if os.geteuid() != 0:
       print("run as root")
       exit(-1)

def bool_to_status(bool_value):
    if bool_value:
        return "OK"
    else:
        return "Err"


class Linux_dns_util:

    @staticmethod
    def get_resolv_conf() -> str:
        resolv_conf_content =   "# Writed by shecan-cli \n"
        resolv_conf_content += f"# your previous dns config is in {dns_file_bak}\n"
        resolv_conf_content += f"# you can restore your dns config by running > shecan-cli disable\n\n"
        for dns_server in shecan_dns:
            resolv_conf_content += f"nameserver {dns_server}\n"
        return resolv_conf_content

    @staticmethod
    def local_status() -> bool:
        file = open(dns_file,"r")
        content = file.read()
        file.close()
        if content == Linux_dns_util.get_resolv_conf():
            return True
        else:
            return False
    
    @staticmethod
    def enable():
        check_root()
        # backup
        os.system(f'cp {dns_file} {dns_file_bak}') 

        #enable
        file = open(dns_file,"w")
        file.write(Linux_dns_util.get_resolv_conf())
        file.close()
        print("shecan enabled")

    @staticmethod
    def disable():
        check_root()
        os.system(f"mv {dns_file_bak} {dns_file}")
        print("shecan disabled")


class Darwin_dns_util:

    @staticmethod
    def get_dns_list() -> str:
        result = ""
        for dns_server in shecan_dns:
            result+=dns_server + " "
        return result

    @staticmethod
    def local_status() -> bool:
        result = os.popen(f"networksetup -getdnsservers {interface}").read()
        return Darwin_dns_util.get_dns_list() == result 
    
    @staticmethod
    def enable():
        # backup
        result = os.popen(f"networksetup -getdnsservers {interface}").read()
        f = open(dns_file_bak,"w")
        f.write(result)

        # enable
        os.system(f"networksetup -setdnsservers {interface} {Darwin_dns_util.get_dns_list()}")
        pass

    @staticmethod
    def disable():
        f = open(dns_file_bak,"r")
        old_dns = f.read()
        os.system(f"networksetup -setdnsservers {interface} {old_dns}")
        pass


def enable():
    if platform=="Linux":
        Linux_dns_util.enable()
    elif platform=="Darwin":
        Darwin_dns_util.enable()
    else:
        print(f"{platform} is not supported")

def disable():
    if platform=="Linux":
        Linux_dns_util.disable()
    elif platform=="Darwin":
        Darwin_dns_util.disable()
    else:
        print(f"{platform} is not supported")

def local_status():
    if platform=="Linux":
        Linux_dns_util.local_status()
    elif platform=="Darwin":
        Darwin_dns_util.local_status()
    else:
        print(f"{platform} is not supported")

def ping_status():
    try:
        r = requests.get("http://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

def remote_status():
    try:
        r = requests.get(shecan_check_url, timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

def status():
    print("local\t\tping\t\tisShecanized")
    print(bool_to_status(local_status())+"\t\t",end="")
    print(bool_to_status(ping_status())+"\t\t",end="")
    print(bool_to_status(remote_status())+"\t\t")

def live_status():
    while True:
        try:
            os.system('clear')
            status()
            sleep(2)
        except KeyboardInterrupt:
            exit(0)

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