import requests

url = 'http://192.168.2.28:8080/set_content/Test%20Subject/Body%20Test'
# url = 'http://192.168.1.5:8080/set_email/nkemme54@gmail.com/'

x = requests.get(url)
print(x.text)