# RESTful-API
## About
This is a REST API that uses Python with Flask and SQLAlchemy, with get, put, patch, and delete functions.

## Getting Started
You will need Python and Pip installed. Then open the project in Visual Studio Code, and in the terminal type:
`pip install -r requirements.txt`
Now you can run main.py and test.py via:
`python main.py`
and opening up another terminal and entering:
`python test.py`

## Example
You may pass arguments in the response line in test.py, for example:
```python
response = requests.get(BASE + "video?id=1")
```
will return the video whose id is 1 when you run test.py in the terminal.
Other examples are:
* Get all videos: ```response = requests.get(BASE + "video")```
* Get videos via name search (uses fuzzy logic): ```response = requests.get(BASE + "video?name=For+You")```
* Insert a new video(id, name, views, and likes are required): ```response = requests.put(BASE + "video?id=6&name=Six+Feet+Under&views=66&likes=6")```
* Update a video(only id is required): ```response = requests.patch(BASE + "video?id=6&name=Sixty+Seconds")```
* Delete a video(id is required): ```response = requests.delete(BASE + "video?id=5")```
