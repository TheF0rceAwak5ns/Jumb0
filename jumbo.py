import requests

def login(user, password, url):
    urll = f'{url}wp-login.php'
    data = {
        'log': user,
        'pwd': password,
        'wp-submit': 'Log+In',
        'redirect_to': f'{url}/wp-admin/index.php',
        'testcookie': '1'
    }  
    r = requests.post(url=urll, data=data,  allow_redirects=True)
    if r.status_code == 200:  
        return True
    else: 
        return False


user = input('enter wp user: ')
password = input('enter wp pass: ')
url = input('enter wp url: ')
login_wp = login(user, password, url) 
print(login_wp)
