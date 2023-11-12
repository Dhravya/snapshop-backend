import requests
from time import sleep

while True:
    response = requests.get('https://dropit2-production.up.railway.app/googleSearch?itemName=White Dress Shirt Women')
    print(response.text)
    sleep(10)

