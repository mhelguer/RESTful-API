import requests
from requests.api import request
        
# location of api's server
BASE = "http://127.0.0.1:5432/"

response = requests.put(BASE + "video/1", {"likes": 10})
response.close()

# print the response, json makes it not look like
# a response object
print(response.json())