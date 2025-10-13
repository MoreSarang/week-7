'''
Script to load geographical data into a pandas DataFrame,
and save it as a CSV file.
'''
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim


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


def fetch_location_data(geolocator, loc):
    """
    Fetch location data for a given location string.

    Parameters
    ----------
    geolocator : Nominatim
        The geolocator instance to use
    loc : str
        The location string to geocode

    Returns
    -------
    dict
        Dictionary with location data, or NaN values if location not found
    """
    try:
        location = geolocator.geocode(loc)
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
    geo_data = [fetch_location_data(geolocator, loc) for loc in locations]
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
