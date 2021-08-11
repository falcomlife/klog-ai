import requests as requests

class Http():

    def __init__(self, url=None, **param):
        self.url = url
        for key, value in param.items():
            self.url = self.url + "&" + key + "=" + value

    def set(self, url, **param):
        self.url = url
        for key, value in param.items():
            self.url = self.url + "&" + key + "=" + value

    def get(self):
        return requests.get(self.url)
