import requests

class APIRequest:

    def __init__(self, url) -> None:
        self._url = url

    @property
    def url(self):
        return self._url

    def get_data(self):
        try:
            response = requests.get(self._url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            return e