from rest_client import ImageRestClient

rc = ImageRestClient("http://localhost:8000")
rc.upload_image("test_image.jpg")

