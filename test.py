import requests
        
# location of api's server
BASE = "http://127.0.0.1:5000/"

response = requests.patch(BASE + "video?id=5&name=FIVE+Part+2&views=25&likes=10")
response.close()

# print the response, json makes it not look like
# a response object
print(response.json())