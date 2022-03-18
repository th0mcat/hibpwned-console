# hibpwned-console

A terminal-program for https://github.com/plasticuproject/hibpwned

## Installation 

  · Clone the repo.  
  
    user@host:~$ git clone https://github.com/th0mcat/hibpwned-console
    user@host:~$ cd hibpwned-console
    
  · (Optional) Create a virtual environment
  
    user@host:~$ virtualenv -p /usr/bin/python3 .venv
    user@host:~$ source .venv/bin/activate
    
  · Install the dependencies.

    user@host:~$ pip install -r requirements.txt
  
  · Set API key in global environment (and, optionally, the `app_name`.)
  
    user@host:~$ export HIBP_API_KEY=<api_key> [HIBP_APP=<app_name>] 

  · Run the program.  

    user@host:~$ python3 hibpwned-console
  
## Roadmap

Eventually, this will be used to create a [maubot](https://github.com/maubot/maubot) plugin and/or an [opsdroid](https://github.com/opsdroid/opsdroid) skill.  
