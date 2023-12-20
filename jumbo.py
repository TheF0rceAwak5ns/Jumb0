import requests
import argparse
from bs4 import BeautifulSoup

# WORDPRESS

# JOOMLA
def getHiddenValues(url):
    
    response = requests.get(f"{url}/index.php")
    
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


def postLoginJoomla(user, password, url, hidden_values):
    
    data = {
        'username': user,
        'password': password,
        'Submit=': '',
        'option': hidden_values.get('option', ''),
        'task': hidden_values.get('task', ''),
        'return': hidden_values.get('return', ''),
        hidden_values.get('1', ''): '1'
    }
    
    response = requests.post(url, data, allow_redirects=True)
    print(f'[+] {data}')
    print(f'[+] Status code: {response.status_code}')

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
            print('Mode: wordpress')
        elif args.mode == 'joomla':
            print('Mode: joomla')
    else:
        print("No CMS mode specified. Please choose a CMS mode: wordpress or joomla.")

if __name__ == "__main__":
    main()
