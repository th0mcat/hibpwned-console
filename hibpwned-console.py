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
import pyfiglet
import sys

from getpass import getpass
from os import environ
from time import sleep

# Email to check breaches for
HIBP_EMAIL = None # Will request email later.

# haveibeenpwned credentials
HIBP_APP = environ.get("HIBP_APP") or "hibpwned-console" # Pulls app_name from environment or uses 'hibpwned-console'
HIBP_API_KEY = environ.get("HIBP_API_KEY") or None # Pulls API key from environment

# Making the API call through hibpwned
hibpconsole = hibpwned.Pwned(HIBP_EMAIL, HIBP_APP, HIBP_API_KEY)

# Search HIBP_EMAIL in all breaches
def all_breaches_single():
    # Ask to search for unverified breaches and truncated output.
    options_trnk = {
        "y": ",truncate=True", # First comma is necessary if options_unver[HIBP_UNVER] == y
        "n": ""
    }
    options_unver = {
        "y": "unverified=True",
        "n": ""
    }
    more = "y"
    while more == "y":
        HIBP_EMAIL = str.lower(input("Enter the email address of the account you wish to check: "))
        HIBP_TRNK = str.lower(input("Do you want the results to be trunkcated? (y/n) "))
        HIBP_UNVER = str.lower(input("Do you want to search unverified breaches? (output will always be truncated) (y/n) "))
        hibpconsole = hibpwned.Pwned(HIBP_EMAIL, HIBP_APP, HIBP_API_KEY)
        print()
        try:
            print(json.dumps(hibpconsole.search_all_breaches(options_unver[HIBP_UNVER]+options_trnk[HIBP_TRNK]), indent=4))
        except ValueError: 
            print("Invalid option")
        print()
        more = input("Do you want to check another email address? (y/n) ")

# Copy/paste a line-separated list of email addresses        
def all_breaches_list():
    more = "y"
    while more == "y":
        print("Copy/Paste the list of emails into this terminal. Results will search unverified breaches")
        print("and be truncated. Hit 'Ctrl + D' when finished. ")
        email_list = sys.stdin.read().splitlines()
        print()
        for i in email_list:
            hibpconsole = hibpwned.Pwned(i, HIBP_APP, HIBP_API_KEY)
            print(i)
            print(json.dumps(hibpconsole.search_all_breaches(unverified=True,truncate=True), indent=4))
            sleep(2)
        more = input("Do you want to check another list of emails? (y/n) ")

# Check a password against breaches
def pass_check():
    more = "y"
    while more == "y":
        check_pass = getpass(prompt='Enter password to check against breaches: ')
        check_pass_num = int(hibpconsole.search_password(check_pass))
        if check_pass_num > 0:
            print(f"The password has been exposed {check_pass_num} time(s) in data breaches.  You should change it.")
        else:
            print("This password has not been found in any known data breaches.")
        more = input("Do you want to check another password? (y/n) ")

# Dictionary of all possible options
options = {
    1: all_breaches_single,
    2: all_breaches_list,
    3: pass_check,
    4: quit
}

def main():
    choice = 1
    while choice != 4:
        HIBP_BANNER = pyfiglet.figlet_format("hibpwned-console", width = 200)
        print("\n\n\n", HIBP_BANNER, "\n\n\n1) Search all breaches for single account\n2) Search all breaches for a list of accounts\n3) Check password for exposure\n4) Quit\n")
        choice = int(input("Please choose an option: "))
        try:
            options[choice]()
        except KeyError: 
            print("Invalid option")
        

if not all([HIBP_API_KEY]): 
    print("API key not declared in global environment or in script.  Please declare the API key and try again.")
    exit(0)

if __name__ == '__main__':
    main()
