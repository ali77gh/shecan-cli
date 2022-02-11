#!/usr/bin/env python3

import os
import sys
import requests
import platform
import os.path
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
dns_file_bak_mac = "/var/root/.shecan-cli"


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
        if Linux_dns_util.local_status():
            print("shecan is already enabled")
            exit(0)

        # backup
        os.system(f'cp {dns_file} {dns_file_bak}') 

        #enable
        file = open(dns_file,"w")
        file.write(Linux_dns_util.get_resolv_conf())
        file.close()
        print("shecan enabled")

    @staticmethod
    def disable():
        if not os.path.isfile(dns_file_bak):
            print("shecan is already disabled")
            exit(0)
        os.system(f"mv {dns_file_bak} {dns_file}")
        print("shecan disabled")


class Darwin_dns_util:

    def get_current_dns():
        return os.popen(f"networksetup -getdnsservers {interface}").read().replace("\n", " ")

    @staticmethod
    def get_shecan_dns_list() -> str:
        return " ".join(shecan_dns) + " "

    @staticmethod
    def local_status() -> bool:
        return Darwin_dns_util.get_shecan_dns_list() == Darwin_dns_util.get_current_dns()
    
    @staticmethod
    def enable():
        # backup
        f = open(dns_file_bak_mac,"w")
        f.write(Darwin_dns_util.get_current_dns())

        # enable
        os.system(f"networksetup -setdnsservers {interface} {Darwin_dns_util.get_shecan_dns_list()}")
        pass

    @staticmethod
    def disable():
        f = open(dns_file_bak_mac,"r")
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
        return Linux_dns_util.local_status()
    elif platform=="Darwin":
        return Darwin_dns_util.local_status()
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

def show_permission_error():
    print("┌───────────────────────────────────────────────────────┐")
    print("│ Permission denied. you may need to run with 'sudo'    │")
    print("└───────────────────────────────────────────────────────┘")

def show_help():
    print("┌────────────────────────────────────────────────────────┐");
    print("│                        shecan-cli                      │");
    print("│ > https://github.com/ali77gh/shecan-cli                │");
    print("│                                                        │");
    print("├────────────────────────────┬───────────────────────────┤");
    print("│ > how to use:              │                           │");
    print("│   shecan-cli help          │ show this beautiful msg   │");
    print("│   shecan-cli status        │ show status (local&remote)│");
    print("│   shecan-cli enable        │ enables shecan DNS        │");
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
        try:
            main_switch(sys.argv[1])
        except PermissionError:
            show_permission_error()


if __name__ == '__main__':
    main()
