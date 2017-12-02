import unittest
from rest_client import ImageRestClient
from tensorflow_prediction import predict_image, load_graph

class Test_rest_client_unit_test(unittest.TestCase):
    #def try_upload_image(self):
    #    rc = ImageRestClient()
    #    rc.upload_image("localhost:8000","test_image.jpg")
    #    self.assertEqual('foo'.upper(), 'FOO')

    def test_upper(self):
        rc = ImageRestClient("http://localhost:8000")
        val = rc.upload_image("test_image.jpg")
        self.assertEqual(val, 0)

    def test_tensorflow(self):
        graph = load_graph("output_graph.pb")
        predict = predict_image("test_cat_image.jpg", graph)
        self.assertEqual(predict[0][0], "cats")

if __name__ == '__main__':
    unittest.main()





