import unittest
from rest_client import ImageRestClient

class Test_rest_client_unit_test(unittest.TestCase):
    #def try_upload_image(self):
    #    rc = ImageRestClient()
    #    rc.upload_image("localhost:8000","test_image.jpg")
    #    self.assertEqual('foo'.upper(), 'FOO')

    def test_upper(self):
        rc = ImageRestClient("http://localhost:8000")
        val = rc.upload_image("test_image.jpg")
        self.assertEqual(val, 0)

if __name__ == '__main__':
    unittest.main()





