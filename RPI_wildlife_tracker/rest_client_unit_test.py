import unittest
from rest_client import ImageRestClient

class Test_rest_client_unit_test(unittest.TestCase):
    def try_upload_image(self):
        rc = ImageRestClient()
        rc.upload_image("localhost:8000","test_image.jpg")
        

if __name__ == '__main__':
    unittest.main()





