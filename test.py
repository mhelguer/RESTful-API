import requests
        
# location of api's server
BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "video?name=video")        
response.close()

# print the response, json makes it not look like
# a response object
print(response.json())