import requests
from logging import Logger
from datetime import date
from utils import jsonUtils, UserInfo, Path


class Diagnosis:
    def __init__(self, user: UserInfo, logger: Logger, testing = True) -> None:
        self.user = user
        self.logger = logger
        self.testing = testing

    def _get_token(self) -> str:
        '''Make call to APImedic to get token'''
        
        import hmac
        import base64
        import hashlib
        
        url = f"https://{'sandbox-' if self.testing else ''}authservice.priaid.ch/login"
        api_key = "1000438@lcps.org" if self.testing else self.user.api_username
        secret_key = "a7N8Dxe9BAd4n6S3M" if self.testing else self.user.api_password
        
        hashed: hmac.HMAC = hmac.new(
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

    def make_call(self, file: Path = None):
        token = self._get_token()
        file = Path(file) if file is not None else Path(date.today().strftime("json/health/%d_%m_%y.json"))
        
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
    
