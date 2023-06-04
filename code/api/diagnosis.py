from utils.parse_json import jsonUtils
from utils.data_classes import UserInfo
import requests


class Diagnosis:
    def __init__(self, user: UserInfo) -> None:
        self.user = user

    @property
    def _token(self):
        return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjEwMDA0MzhAbGNwcy5vcmciLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6Ijk0MDIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3ZlcnNpb24iOiIxMDkiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xpbWl0IjoiMTAwIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwIjoiQmFzaWMiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xhbmd1YWdlIjoiZW4tZ2IiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDk5LTEyLTMxIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwc3RhcnQiOiIyMDIzLTAzLTI4IiwiaXNzIjoiaHR0cHM6Ly9hdXRoc2VydmljZS5wcmlhaWQuY2giLCJhdWQiOiJodHRwczovL2hlYWx0aHNlcnZpY2UucHJpYWlkLmNoIiwiZXhwIjoxNjg1OTAwNzE3LCJuYmYiOjE2ODU4OTM1MTd9.AmoDtWdf-bDS7f20_qWx9vXqZM6Byz4zryNcBAzKb20"

    def make_call(self, file: str = "json/possible_diseases.json"):
        # Set the API endpoint and parameters
        url = "https://healthservice.priaid.ch"
        action = "/diagnosis"
        token = self._token
        language = "en-gb"



        # Set the query parameters
        params = {
            "token": token,
            "language": language,
            "symptoms": str(self.user.conditions),
            "gender": str(self.user.gender),
            "year_of_birth": str(self.user.birthyear)
        }

        # Make a GET request to the API endpoint
        # response = requests.get(url + action, params=params)
        response = requests.get(
            "https://healthservice.priaid.ch/diagnosis?symptoms={0}&gender={1}&year_of_birth={2}&token={3}&format=json&language={4}".format(
                params["symptoms"], params["gender"], params["year_of_birth"], params["token"], params["language"]
            )
            )
        jsonUtils.overwrite(response.json(), file)
        return jsonUtils.open(file)


if __name__ == "__main__":
    diag = Diagnosis("")
    print(diag.make_call())
    
