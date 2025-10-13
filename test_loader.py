import unittest

import numpy as np
import pandas as pd

from loader import build_geo_dataframe, fetch_location_data, get_geolocator


class TestLoader(unittest.TestCase):
    def test_valid_locations(self):
        """Test that valid locations are correctly geocoded."""
        geolocator = get_geolocator()
        
        # Test Museum of Modern Art
        moma_result = fetch_location_data(
            geolocator, 
            "Museum of Modern Art"
        )
        self.assertEqual(
            moma_result["location"], 
            "Museum of Modern Art"
        )
        self.assertAlmostEqual(
            moma_result["latitude"], 
            40.7618552, 
            places=2,
            msg="MoMA latitude should be approximately 40.76"
        )
        self.assertAlmostEqual(
            moma_result["longitude"], 
            -73.9782438, 
            places=2,
            msg="MoMA longitude should be approximately -73.98"
        )
        self.assertEqual(
            moma_result["type"], 
            "museum"
        )
        
        # Test USS Alabama Battleship Memorial Park
        uss_result = fetch_location_data(
            geolocator, 
            "USS Alabama Battleship Memorial Park"
        )
        self.assertEqual(
            uss_result["location"], 
            "USS Alabama Battleship Memorial Park"
        )
        self.assertAlmostEqual(
            uss_result["latitude"], 
            30.684373, 
            places=2,
            msg="USS Alabama latitude should be approximately 30.68"
        )
        self.assertAlmostEqual(
            uss_result["longitude"], 
            -88.015316, 
            places=2,
            msg="USS Alabama longitude should be approximately -88.02"
        )
        self.assertEqual(
            uss_result["type"], 
            "park"
        )

    def test_invalid_location(self):
        """Test that invalid locations return NaN values."""
        geolocator = get_geolocator()
        result = fetch_location_data(geolocator, "asdfqwer1234")
        
        # Check that location name is preserved
        self.assertEqual(
            result["location"], 
            "asdfqwer1234",
            "Location name should be preserved even for invalid locations"
        )
        
        # Check that latitude is NaN
        self.assertTrue(
            pd.isna(result["latitude"]),
            "Latitude should be NaN for nonexistent location"
        )
        
        # Check that longitude is NaN
        self.assertTrue(
            pd.isna(result["longitude"]),
            "Longitude should be NaN for nonexistent location"
        )
        
        # Check that type is NaN
        self.assertTrue(
            pd.isna(result["type"]),
            "Type should be NaN for nonexistent location"
        )


if __name__ == "__main__":
    unittest.main()
