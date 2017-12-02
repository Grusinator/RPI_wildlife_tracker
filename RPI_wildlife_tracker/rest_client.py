#import httplib
import json
import requests
from requests.auth import HTTPBasicAuth


class ImageRestClient():
    auth = None
    def __init__(self, domain):
        self.domain = domain

    def upload_image(self, path, title="test1", desc=""):

        url = self.domain + "/api/images/"
        files = {'image': open(path, 'rb')}

        values = {
            "title": title,
            "description": desc,
        }
        try:
            requests.post(url,  data=values, files=files)
        except Exception as e:
            print("Error: Error in http request!")
            print(e)
            return 1
        return 0

    def login(self, username, password):

        body = {
            "username": username,
            "password": password,
        }

        result = self.post("api/users/login/", body=body)

        self.auth = HTTPBasicAuth(username, password)

        try:
            return str(result["auth_token"])
        except Exception as e:
            print("Error: Error in http request!")
            print(e)


    def signup(self, username, password):
        body = {
            "username": username,
            "password": password,
            "password_again": password,
        }

        result = self.post("api/users/register/", body=body)
        self.auth = HTTPBasicAuth(username, password)

        try:
            return str(result["auth_token"])
        except Exception as e:
            print("Error: Error in http request!")
            print(e)


    def get(self,url,body=None):
        if isinstance(body, str):
            body = json.dumps(body)
        elif isinstance(body, dict):
            pass

        try:
            result = requests.get(self.domain+url, auth=self.auth, params=body)
            return json.loads(result.text)

        except Exception as e:
            print("Error: Error in http request!")
            print(e)

    def post(self,url,body=None):
        if isinstance(body, str):
            body = json.dumps(body)
        elif isinstance(body, dict):
            pass

        try:
            result = requests.post(self.domain+url, data=body, auth=self.auth)
            return json.loads(result.text)


        except Exception as e:
            print("Error: Error in http request!")
            print(e)


    #def httprequest(self, type='GET', url="",body=None, ):
    #    try:
    #        connection = httplib.HTTPConnection(self.domain)
    #        connection.connect()


    #        connection.putheader()
    #    except:
    #        print("Error: Unable to connect!")

    #    header = {
    #       "Content-Type": "application/json"
    #    }

    #    result = "not received"
    #    try:
    #        connection.request('POST', url , body=body, headers=header )
    #        result = json.loads(connection.getresponse().read())
    #        return result

    #    except Exception as e:
    #        print("Error: Error in http request!")
    #        print(e)
    #        print(result)
