import requests
import json

def foo():
    # Set the API endpoint and parameters
    url = "https://sandbox-healthservice.priaid.ch"
    action = "/diagnosis"
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjEwMDA0MzhAbGNwcy5vcmciLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IjEyMDM2IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMjAwIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6Ijk5OTk5OTk5OSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IlByZW1pdW0iLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xhbmd1YWdlIjoiZW4tZ2IiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDk5LTEyLTMxIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwc3RhcnQiOiIyMDIzLTAzLTI4IiwiaXNzIjoiaHR0cHM6Ly9zYW5kYm94LWF1dGhzZXJ2aWNlLnByaWFpZC5jaCIsImF1ZCI6Imh0dHBzOi8vaGVhbHRoc2VydmljZS5wcmlhaWQuY2giLCJleHAiOjE2ODM0MzM3NjEsIm5iZiI6MTY4MzQyNjU2MX0.-8d8DKn9hN2BTb8D9V05Potb9SdCnenQrm_cFnY_zMk"
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
    print(response.json())
foo()
# Print the response content
# with open("json_files/symptoms.json", "w") as f:
#     f.write(json.dumps(response.json(), indent=4))

# with open("json_files/symptoms.json") as f:
#     data = json.load(f)
#     data.sort(key=lambda x: int(x["ID"]))
#     print("\n".join(map(str, data)))
    
# with open("json_files/symptoms.json", "w") as f:
#     f.write(json.dumps(data, indent=4))