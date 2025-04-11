import sys
import os
import json
from flask import Flask
from flask_jwt_extended import JWTManager

# Add the project root directory to sys.path for imports to work correctly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import control.activity_controller as activity_controller

import unittest

class TestItineraryController(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.activity_controller = activity_controller
    
    
    def test_get_all_activities(self):
        activities = self.activity_controller.internal_get_all_activities()
        
        self.assertNotEqual(None, activities)
      
        
    def test_get_activity_by_id(self):
        activity = json.loads(self.activity_controller.internal_get_activity_by_id(
            id = 1
        ))
        self.assertEqual("Raffles Singapore", activity["Name"])
        self.assertEqual("Cultural & Heritage", activity["Type"])
        self.assertEqual("1 Beach Road", activity["Location"])
        self.assertEqual("0.0", activity["Price"])
        self.assertEqual("Free", activity["Price Category"])
        self.assertEqual("https://www.google.com/maps?q=1%20Beach%20Road&output=embed", activity["Image"])
        self.assertEqual("""Raffles Singapore, a name synonymous with colonial grandeur, stands proudly at 1 Beach Road as a living testament to Singapore's rich cultural and heritage tapestry. More than just a luxury hotel, it's a national monument, a time capsule meticulously preserved and celebrated. Stepping through its doors is like stepping back into a bygone era, where ceiling fans whirred and the aroma of afternoon tea filled the air.

While not a traditional school, imagine the manicured lawns surrounding Raffles as a sophisticated sports field, where generations have indulged in croquet and leisurely pursuits. The hotel's architecture, with its white facade and stately columns, speaks of a colonial past, while its meticulously maintained gardens offer a serene escape from the bustling city.

Raffles is a repository of stories, hosting literary giants, royalty, and dignitaries for over a century. It’s a place where history is not just read about, but experienced, making it a cornerstone of Singapore's cultural identity and a must-see for anyone seeking a glimpse into the nation's captivating past.
""",activity["Description"])
        
    
    def test_get_activities_by_type(self):
        activities = self.activity_controller.internal_get_activities_by_type(
            type = "Outdoor & Nature"
            )
        
        for activity in activities:
            activity_type = json.loads(activity)["Type"]
            self.assertEqual("Outdoor & Nature", activity_type)
            
            
    def test_get_activities_by_price_category(self):
        activities = self.activity_controller.internal_get_activities_by_price_category(
            category = "$$$"
            )
        
        for activity in activities:
            price_category = json.loads(activity)["Price Category"]
            self.assertEqual("$$$", price_category)
            
    
    def test_get_activities_by_type_and_price_category(self):
        activities = self.activity_controller.internal_get_activities_by_type_and_price_category(
            type = "Workshops & Classes",
            category = "$$$"
            )
        
        for activity in activities:
            formatted_activity = json.loads(activity)
            activity_type = formatted_activity["Type"]
            self.assertEqual("Workshops & Classes", activity_type)
            price_category = formatted_activity["Price Category"]
            self.assertEqual("$$$", price_category)
        
        
if __name__ == "__main__":
    unittest.main() 