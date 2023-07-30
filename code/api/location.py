from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderQueryError
from logging import Logger
from typing import Coroutine, Callable

def _test_availiable(result: Callable[[], type[object]], /, logger: Logger) -> type[object]:
    '''Test if geocoder is unavailable (raise `GeocoderUnavailable` exception) or if result is null (raise `GeocoderQueryError`)'''
    try:
        x = result()
    except GeocoderUnavailable as g:
        logger.warning("Geocoder service unavailable right now")
        flag = True
        msg = g
    else:
        flag = False
    finally:
        if flag:
            raise GeocoderUnavailable(msg)
        
    if x is None:
        raise GeocoderQueryError("Result from geocoder was null")
    return x

def get_location(geocode: str, logger: Logger) -> Coroutine:
    '''Return geocode object based on geocode.
    
    Args:
    -----
        geocode (str): location.
            Ex) Ashburn Virginia
        logger (Logger): logger to output information to.
            
    Returns:
    --------
        Coroutine: if successful, an object that contains `ob.address`, `ob.latitude`, and `ob.longitude` properties
            
    Raises:
    -------
        geopy.exc.GeocoderUnavailiable: Geocoder service is unavailiable
        geopy.exc.GeocoderQueryError: Result from geocoder service was null
    '''
    # https://www.geeksforgeeks.org/how-to-get-geolocation-in-python/
    # method 1
    return _test_availiable(
            lambda: Nominatim(user_agent="GetLoc").geocode(geocode),
            logger
        )
    

def coords_to_address(latitude: float, longitude: float, logger: Logger, *, no_zip: bool = False) -> str:
    '''Convert latitude and longitude coords to relative address
    
    Returns:
    --------
        str: City, County, State, Zip, Country. If `no_zip` is `True`, zip is not included
            
    Raises:
    -------
        geopy.exc.GeocoderUnavailiable: Geocoder service is unavailiable
        geopy.exc.GeocoderQueryError: Result from geocoder service was null
    '''
    address = _test_availiable(
            lambda: Nominatim(user_agent="GetLoc").reverse(f"{latitude}, {longitude}"),
            logger
        )
    delimiter = ", "
    datas = str(address).split(delimiter)[3:]
    
    if no_zip:
        try:
            datas.pop(-2)
        except IndexError:
            logger.error("An IndexError occured while trying to remove zip code. Try checking output from Nominatim.reverse")
            exit(1)
    
    address = delimiter.join(datas) # crop off address due to imprecision
    return address


def main():
    l = get_location("Ashburn Virginia", Logger(__name__))
    print(l)
    lat, long = l.latitude, l.longitude
    print(coords_to_address(lat, long, Logger(__name__), no_zip=True))

if __name__ == "__main__":
    main()
