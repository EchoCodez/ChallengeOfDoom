from geopy.geocoders import Nominatim
from typing import Coroutine

def get_location(geocode: str) -> Coroutine:
    '''Return geocode object based on geocode.
    
    Args:
    -----
        geocode (str): location.
            Ex) Ashburn Virginia'''
    # https://www.geeksforgeeks.org/how-to-get-geolocation-in-python/
    # method 1
    return Nominatim(user_agent="GetLoc").geocode(geocode)

if __name__ == "__main__":
    print(get_location("Ashburn Virginia").address)
