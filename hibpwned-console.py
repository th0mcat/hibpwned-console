# A Terminal program for https://github.com/plasticuproject/hibpwned
#
# Copyright (C) 2022  me@thomcat.rocks
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import hibpwned
import json
import hashlib
from getpass import getpass

# Email to check breaches for
HITB_EMAIL = #<email>

# haveibeenpwned credentials
HITB_APP = #<app_name>
HITB_API_KEY = #<api_key>

# Making the API call through hibpwned
hibpconsole = hibpwned.Pwned(HITB_EMAIL, HITB_APP, HITB_API_KEY)

# Search HIBP_EMAIL in all breaches
def all_breaches():
    # Ask to search for unverified breaches and truncated output.
    options_trnk = {
        "y": ",truncated=True", # First comma is necessary if options_unver[HIBP_UNVER] == y
        "n": ""
    }
    options_unver = {
        "y": "unverified=True",
        "n": ""
    }
    HIBP_TRNK = str.lower(input("Do you want the results to be trunkcated? (y/n) "))
    HIBP_UNVER = str.lower(input("Do you want to search unverified breaches? (output will always be truncated) (y/n) "))
    print(options_unver[HIBP_UNVER]+options_trnk[HIBP_TRNK])
    try:
        print(json.dumps(hibpconsole.search_all_breaches(options_unver[HIBP_UNVER]+options_trnk[HIBP_TRNK]), indent=4))
    except ValueError: 
        print("Invalid option")

# Check a password against breaches
def pass_check():
    check_pass = getpass(prompt='Enter password to check against breaches: ')
    check_pass_num = int(hibpconsole.search_password(check_pass))
    if check_pass_num > 0:
        print(f"The password has been exposed {check_pass_num} time(s) in data breaches.  You should change it.")
    else:
        print("This password has not been found in any known data breaches.")

options = {
    1: all_breaches,
    2: pass_check
}

def main():
    print("\n1) Search all breaches\n2) Check password for exposure\n")
    choice = int(input("Please choose an option: "))
    try:
        options[choice]()
    except KeyError: 
        print("Invalid option")

if __name__ == '__main__':
    main()
