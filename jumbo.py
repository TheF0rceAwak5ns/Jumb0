import sys
import requests
import argparse
from rich.console import Console
from rich.text import Text
from bs4 import BeautifulSoup
console = Console()


# State with colors
# Todo : put this in POO class message.entry message.success etc.. for practice and good code
def tool_entry():
    return console.print("[u]Jumbo[/u] >", style="bold")
def ongoing():
    return console.print("[*]", style="bold blue")

def success():
    message = Text("[+]", style="bold green")
    return message

def failed():
    return console.print("[-]", style="bold red")

def warning():
    return console.print("[!]", style="bold yellow")

#Wordpress mode 

#login 
def login(user, password, base_url):
    url = f'{base_url}/wp-login.php'
    data = {
        'log': user,
        'pwd': password,
        'wp-submit': 'Log+In',
        'redirect_to': f'{base_url}/wp-admin/index.php',
        'testcookie': '1'
    }  
    response = requests.post(url, data,  allow_redirects=True)
    if response.status_code == 200:  
        print(response)
        return True
    else: 
        return False



# argparse
def main():
    parser = argparse.ArgumentParser(description='Jumbo loves to put some RCE in CMS')

    # Choose your CMS MODE
    parser.add_argument('mode', choices=['wordpress', 'joomla'], help='Choose a CMS mode: wordpress or joomla', nargs='?')

    # Options for WordPress & Joomla
    parser.add_argument('-u', '--username', dest='username', help='username')
    parser.add_argument('-p', '--password', dest='password', help='password')
    parser.add_argument('-H', '--host', dest='host', help='CMS website HOST')
    # TODO : add option to change the USER-AGENT ?

    args = parser.parse_args()

    if args.mode:
        if args.mode == 'wordpress':
            console.print(success(), "Mode: wordpress")
            login_wp = login(args.username, args.password, args.host)
            print(login_wp)
        elif args.mode == 'joomla':
            print(f'{success()} Mode: joomla')
            hidden_values = get_hidden_values(args.host)
            post_login_joomla(args.username, args.password, args.host, hidden_values)
    else:
        print("No CMS mode specified. Please choose a CMS mode: wordpress or joomla.")


if __name__ == "__main__":
    main()