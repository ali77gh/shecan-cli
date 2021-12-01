#!/bin/python3

import os
import sys

def check_root():
    return os.geteuid() == 0

def disable():
    os.exec("cat /etc/resolv.conf.bak > /etc/resolv.conf")

def enable():
    os.exec()

def status():
    pass

def local_check():
    pass

def remote_check():
    pass

def live_status():
    pass

def uninstall():
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
    pass

def main_switch():
    pass

def main():
    print(sys.argv);
    if len(sys.argv) != 2:
        show_help()
    else:
        main_switch()


main()