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
    text = r.text
    print(r.text)


user = input('enter wp user: ')
Password = input('enter wp pass: ')
url = input('enter wp url: ')
login(user, Password, url) 
