'''
Script to load geographical data into a pandas DataFrame,
and save it as a CSV file.
'''
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import numpy as np


def get_geolocator(agent='h501-student'):
    """
    Initiate a Nominatim geolocator instance given an agent.

    Parameters
    ----------
    agent : str, optional
        Agent name for Nominatim, by default 'h501-student'

    Returns
    -------
    Nominatim
        A Nominatim geolocator instance
    """
    return Nominatim(user_agent=agent)


def get_rate_limited_geocoder(geolocator, min_delay=1.0):
    """
    Create a rate-limited geocoder to comply with Nominatim usage policy.

    Parameters
    ----------
    geolocator : Nominatim
        The geolocator instance to wrap
    min_delay : float, optional
        Minimum delay between requests in seconds, by default 1.0

    Returns
    -------
    RateLimiter
        A rate-limited geocoding function
    """
    return RateLimiter(
        geolocator.geocode,
        min_delay_seconds=min_delay,
        max_retries=2,
        error_wait_seconds=5.0,
        swallow_exceptions=True,
        return_value_on_exception=None
    )


def fetch_location_data(geocode_func, loc):
    """
    Fetch location data for a given location string.

    Parameters
    ----------
    geocode_func : callable
        The geocoding function to use (rate-limited)
    loc : str
        The location string to geocode

    Returns
    -------
    dict
        Dictionary with location data, or NaN values if location not found
    """
    try:
        location = geocode_func(loc)
        if location is None:
            return {
                "location": loc,
                "latitude": np.nan,
                "longitude": np.nan,
                "type": np.nan
            }
        return {
            "location": loc,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "type": location.raw.get('type')
        }
    except Exception as e:
        print(f"Error geocoding {loc}: {e}")
        return {
            "location": loc,
            "latitude": np.nan,
            "longitude": np.nan,
            "type": np.nan
        }


def build_geo_dataframe(geolocator, locations):
    """
    Build a pandas DataFrame from a list of locations.

    Parameters
    ----------
    geolocator : Nominatim
        The geolocator instance to use
    locations : list
        List of location strings to geocode

    Returns
    -------
    pd.DataFrame
        DataFrame containing geocoded location data
    """
    # Create rate-limited geocoder
    geocode = get_rate_limited_geocoder(geolocator)
    
    # Geocode all locations with rate limiting
    geo_data = [fetch_location_data(geocode, loc) for loc in locations]
    return pd.DataFrame(geo_data)


if __name__ == "__main__":
    geo = get_geolocator()
    locations = [
        "Museum of Modern Art",
        "iuyt8765(*&)",
        "Alaska",
        "Franklin's Barbecue",
        "Burj Khalifa"
    ]
    df = build_geo_dataframe(geo, locations)
    df.to_csv("./geo_data.csv", index=False)
