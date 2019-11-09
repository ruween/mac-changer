#! /usr/bin/env python

import subprocess
import optparse
import re


# Author : Ruween Iddagoda @almightynewdale
# used to take in the arguments from the command line
def get_arguments(): 
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    # Parse the arguments you get from the user
    (options, arguments) = parser.parse_args()
    # options contains the values that the user inputs
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an MAC address, use --help for info.")
    return options


# function to change the MAC addresses
def change_mac(interface, new_mac):
    print('Changing MAC address for ' + interface + ' to' + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# retrieve the current MAC address to compare and verify the changes
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could'nt get MAC address.")


options = get_arguments()
change_mac(options.interface, options.new_mac)
# print out the results
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + str(current_mac))
else:
    print("[-] MAC address did not change.")



