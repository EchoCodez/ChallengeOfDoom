import requests
from utils import jsonUtils, UserInfo, Path, constants


class Diagnosis:
    def __init__(self, user: UserInfo, testing = True) -> None:
        self.user = user
        self.logger = constants.LOGGER
        self.testing = testing
        self.token = self._get_token()

    def _get_token(self) -> str:
        '''Make call to APImedic to get token'''
        
        import hmac
        import base64
        import hashlib
        
        url = f"https://{'sandbox-' if self.testing else ''}authservice.priaid.ch/login"
        api_key = "1000438@lcps.org" if self.testing else self.user.api_username
        secret_key = "a7N8Dxe9BAd4n6S3M" if self.testing else self.user.api_password
        
        hashed = hmac.new(
            bytes(secret_key, encoding="utf-8"),
            url.encode("utf-8"),
            digestmod=hashlib.md5
            ).digest()
        hashed_credentials = base64.b64encode(hashed).decode()
        
        headers = {
            "Authorization": f"Bearer {api_key+':'+hashed_credentials}"
        }
        response = requests.post(url, headers=headers)
        
        if response.status_code != 200:
            self.logger.error(f"An error occured while fetching user token. Got {response}, expected <Response [200]>")
            print(response.text)
            return ""
        else:
            self.logger.debug("Successfully got token from APImedic")
            token = response.json()['Token']
            return token

    def make_call(self, file: Path | None = None):
        """Make Diagnosis Call"""
        token = self.token
        file = Path(file) if file is not None else constants.TODAY_DATE_FILE
        
        if token == "":
            return ""
        
        # Set the query parameters
        params = {
            "token": token,
            "language": "en-gb",
            "symptoms": str(self.user.conditions),
            "gender": str(self.user.gender),
            "year_of_birth": str(self.user.birthyear),
            "format": "json"
        }

        # Make a GET request to the API endpoint
        response = requests.get(
            "https://{0}healthservice.priaid.ch/diagnosis?symptoms={1}&gender={2}&year_of_birth={3}&token={4}&format={5}&language={6}".format(
                'sandbox-' if self.testing else '',
                params["symptoms"],
                params["gender"],
                params["year_of_birth"],
                params["token"],
                params["format"],
                params["language"]
            )
        )
        jsonUtils.overwrite(response.json(), file)
        return jsonUtils.read(file)
   
    # DO NOT USE THESE METHODS UNLESS DATA IS LOST (SOMEHOW)

    def get_locations(self, file: Path = constants.BODY_LOCATIONS):
        """Get's Body Locations and writes to file. Should only be called again if data is lost"""
        response = requests.get(
                "https://{0}healthservice.priaid.ch/body/locations?token={1}&language={2}&format=json".format(
                'sandbox-' if self.testing else '',
                self.token,
                "en-gb"
            )
        )
        jsonUtils.overwrite(response.json(), file)

    def get_all_sublocations(self, file: Path = constants.BODY_LOCATIONS):
        locations = jsonUtils.read(file)
        for idx, location in enumerate(locations):
            temp = requests.get(
                "https://{0}healthservice.priaid.ch/body/locations/{1}?token={2}&language=en-gb&format=json".format(
                    'sandbox-' if self.testing else '',
                    location["ID"],
                    self.token
                )
            )
            temp = temp.json()
            location["sublocations"] = temp
            locations[idx] = location

        jsonUtils.overwrite(locations, file)

    def get_symptoms_by_sublocation(self, location_id: int, file: Path = constants.CONDITIONS_LIST):
        previous_symptoms = jsonUtils.read(file)
        if previous_symptoms.get(location_id, False):
            return previous_symptoms[location_id]

        previous_symptoms[location_id] = requests.get(
                "https://{0}healthservice.priaid.ch/symptoms/{1}/{2}?token={3}&language=en-gb&format=json".format(
                    'sandbox-' if self.testing else '',
                    location_id,
                    self.user.selector_status,
                    self.token
            )
        ).json()

        jsonUtils.overwrite(previous_symptoms, file)
        return jsonUtils.read(file)
    
    def get_symptoms_by_sublocations(self, *location_ids: int, f: Path = constants.CONDITIONS_LIST):
        return tuple(self.get_symptoms_by_sublocation(id_, file=f) for id_ in location_ids)


