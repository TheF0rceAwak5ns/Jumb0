import requests

#Wordpress mode 

#login 
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


#def write_shell(): 

# send request to connet 
login_wp = login('admin', 'Jumb0%40Ice', 'http://192.168.4.54/')
print(login_wp)


