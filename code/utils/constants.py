"""Constants (typically file paths) used in the code"""

from pathlib import Path
from datetime import date
from logging import getLogger

# Paths
PREFERENCES = Path("json/preferences.json")
USER_DATA = Path("json/user-data.json")
CONDITIONS_LIST = Path("json/symptoms.json")
BODY_LOCATIONS = Path("json/body-locations.json")
MEDICINES = Path("json/medicines.json")
LOGS = Path("json/logs.json")
HEALTH_LOGS = Path("json/health")
CREDENTIALS = Path('json/credentials.json')
TOKEN_FILE = Path('json/token.json')
WEATHER_DATA = Path('json/weather.json')
AIR_QUALITY = Path('json/air-quality.json')
RUNLOG = Path("logs/runlog.log")

# computed every day
TODAY = date.today()
TODAY_DATE_FILE = HEALTH_LOGS / Path(date.today().strftime("%d_%m_%y")).with_suffix(".json")

# Logging
LOGGER_NAME = "CongressionalAppChallenge"
LOGGER = getLogger(LOGGER_NAME)


# Other
IS_TESTING = False

