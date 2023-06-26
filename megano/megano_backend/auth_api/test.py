import requests
import json

url = "http://localhost:8000/product/1"


response = requests.get(url)

print(response.status_code)
print(response.text)
