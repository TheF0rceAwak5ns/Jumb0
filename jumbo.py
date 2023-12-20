import requests
import argparse

def login(user, password, url):
    urll = url
    data = {
        'log': user,
        'pwd': password,
        'wp-submit': 'Log+In',
        'redirect_to': 'url/wp-admin.php',
        'testcookie': '1'
    }  
    r = requests.post(url=urll, data=data)
    text = r.text
    print(r.text)
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
