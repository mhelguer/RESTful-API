import unittest
from main import app

class FlaskTest(unittest.TestCase):
    # Check for get response 200
    def test_index(self):
        tester = app.test_client(self)
        BASE = "http://127.0.0.1:5000/"
        response=tester.get(BASE + "video")         
        statuscode=response.status_code        
        self.assertEqual(statuscode, 200)
    
    # Check if content returned is application/json
    def test_index_content(self):
        tester = app.test_client(self)
        BASE = "http://127.0.0.1:5000/"
        response=tester.get(BASE + "video?name=video") 
        self.assertEqual(response.content_type, 'application/json')
        
    # Check for data returned
    def test_index_data(self):
        tester=app.test_client(self)
        BASE = "http://127.0.0.1:5000/"
        response = tester.get(BASE + "video?name=video")        
        print(response)
        # do not include the brackets at the ends in the comparison    
        self.assertTrue(str(response.data.decode("utf-8")[1:-2]) == '{"id": 1, "name": "First Video", "views": 1, "likes": 0}, {"id": 2, "name": "Second Video", "views": 2, "likes": 2}')
    
    # Check for delete response 200
    def test_delete_video(self):
        tester=app.test_client(self)
        BASE = "http://127.0.0.1:5000/"
        response = tester.delete(BASE + "video?id=5")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check for put response 201
    def test_put_new_video(self):
        tester=app.test_client(self)
        BASE = "http://127.0.0.1:5000/"
        response = tester.put(BASE + "video?id=5&name=FIVE&views=55&likes=5")
        statuscode = response.status_code        
        self.assertEqual(statuscode, 201)
        
    # Check for patch response 200
    def test_patch_video(self):
        tester=app.test_client(self)
        BASE = "http://127.0.0.1:5000/"
        response = tester.patch(BASE + "video?id=3&name=Three+Part+2&views=23&likes=3")
        statuscode = response.status_code        
        self.assertEqual(statuscode, 200)

if __name__=='__main__':
    unittest.main()
