from utils.parse_json import jsonUtils
from utils.data_classes import UserInfo


class Diagnosis:
    def __init__(self, user: UserInfo) -> None:
        self.user = user

    def make_call(self):
        import requests
        import json

        # Set the API endpoint and parameters
        url = "https://sandbox-healthservice.priaid.ch"
        action = "/diagnosis"
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjEwMDA0MzhAbGNwcy5vcmciLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IjEyMDM2IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMjAwIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6Ijk5OTk5OTk5OSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IlByZW1pdW0iLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xhbmd1YWdlIjoiZW4tZ2IiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDk5LTEyLTMxIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwc3RhcnQiOiIyMDIzLTAzLTI4IiwiaXNzIjoiaHR0cHM6Ly9zYW5kYm94LWF1dGhzZXJ2aWNlLnByaWFpZC5jaCIsImF1ZCI6Imh0dHBzOi8vaGVhbHRoc2VydmljZS5wcmlhaWQuY2giLCJleHAiOjE2ODM0ODY5NTksIm5iZiI6MTY4MzQ3OTc1OX0.6F72Ls39EQAqOEz-qLxDzZZlFsU_E7QH5ccbR0s-eo4"
        language = "en-gb"

        # Set the query parameters
        params = {
            "token": token,
            "language": language,
            "symptoms": "[9, 10]",
            "gender": "male",
            "year_of_birth": 1980
        }

        # Make a GET request to the API endpoint
        response = requests.get(url + action, params=params)
        jsonUtils.overwrite(response.json(), "json_files/possible_diseases.json")


if __name__ == "__main__":
    diag = Diagnosis("")
    diag.make_call()
    
