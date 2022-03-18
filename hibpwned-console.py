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
from os import environ
import pyfiglet

# Email to check breaches for
HIBP_EMAIL = environ.get("HIBP_EMAIL") or None # Pulls email from environment

# haveibeenpwned credentials
HIBP_APP = environ.get("HIBP_APP") or None # Pulls app_name from environment
HIBP_API_KEY = environ.get("HIBP_API_KEY") or None # Pulls API key from environment

# Making the API call through hibpwned
hibpconsole = hibpwned.Pwned(HIBP_EMAIL, HIBP_APP, HIBP_API_KEY)

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
    HIBP_BANNER = pyfiglet.figlet_format("hibpwned-console", width = 200)
    print(HIBP_BANNER, "\n1) Search all breaches\n2) Check password for exposure\n")
    choice = int(input("Please choose an option: "))
    try:
        options[choice]()
    except KeyError: 
        print("Invalid option")

if not all([HIBP_EMAIL, HIBP_APP, HIBP_API_KEY]): # all() returns true if every item in the list is a truthy value (i.e, not 0, None or a negative number), false otherwise
    print("Credentials not declared in global environment or in script.  Please enter the credentials and try again.")
    exit(0)

if __name__ == '__main__':
    main()
