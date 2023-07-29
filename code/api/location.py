from geopy.geocoders import Nominatim
from logging import Logger
from typing import Coroutine

def get_location(geocode: str) -> Coroutine:
    return Nominatim(user_agent="GetLoc").geocode(geocode)
    
print(get_location("Ashburn Virginia").address)
