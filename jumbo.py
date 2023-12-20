import requests

def login(user, password, url):
    urll = f'{url}/wp-login.php'
    data = {
        'log': user,
        'pwd': password,
        'wp-submit': 'Log+In',
        'redirect_to': 'url/wp-admin.php',
        'testcookie': '1'
    }  
    r = requests.post(url=urll, data=data)
    status = r.status_code
    if status == 200:  
        get = requests.get(f'{url}/wp-admin/index.php')
        print(get.status_code)
        return True
    else: 
        return False


user = input('enter wp user: ')
password = input('enter wp pass: ')
url = input('enter wp url: ')
login(user, password, url) 
