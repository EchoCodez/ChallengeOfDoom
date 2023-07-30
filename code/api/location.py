from geopy.geocoders import Nominatim
from typing import Coroutine

def get_location(geocode: str) -> Coroutine:
    return Nominatim(user_agent="GetLoc").geocode(geocode)

if __name__ == "__main__":
    print(get_location("Ashburn Virginia").address)
