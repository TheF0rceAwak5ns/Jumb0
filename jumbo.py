import requests

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


login('admin', 'Jumb0%40Ice', 'http://192.168.5.45/wp-login.php')

    