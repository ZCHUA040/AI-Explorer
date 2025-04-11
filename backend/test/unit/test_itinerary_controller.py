import sys
import os
import json
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Add the project root directory to sys.path for imports to work correctly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import control.itinerary_controller as itinerary_controller
import control.activity_controller as activity_controller

import unittest

class TestItineraryController(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.itinerary_controller = itinerary_controller
        self.activity_controller = activity_controller
    
    def test_internal_generate_itinerary(self):
        #All valid input, activites present
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = "Cultural & Heritage",
            price_category = "Free",
            start_time = "0800",
            end_time = "1900"
        )
        itinerary = json.loads(self.itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid["Itineraryid"]))
        
        self.assertEqual(1, itinerary["Userid"])
        self.assertEqual("Unit Testing", itinerary["Title"])
        self.assertEqual("2025-04-10", itinerary["Date"])

        details = json.loads(itinerary["Details"])
        for event in details:
            if "activity" in event.keys():
                activity = json.loads(self.activity_controller.internal_get_activity_by_id(event["id"]))
                self.assertEqual("Cultural & Heritage", activity["Type"])
                self.assertEqual("Free", activity["Price Category"])
        
        self.assertEqual("08:00", details[0]["time"].split("-")[0])
        self.assertEqual("19:00", details[-1]["time"].split("-")[-1])
        
        
        
        #No input for activity_type
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            #activity_type = "Cultural & Heritage",
            price_category = "Free",
            start_time = "0800",
            end_time = "1900"
        )
        itinerary = json.loads(self.itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid["Itineraryid"]))
        
        self.assertEqual(1, itinerary["Userid"])
        self.assertEqual("Unit Testing", itinerary["Title"])
        self.assertEqual("2025-04-10", itinerary["Date"])

        details = json.loads(itinerary["Details"])
        for event in details:
            if "activity" in event.keys():
                activity = json.loads(self.activity_controller.internal_get_activity_by_id(event["id"]))
                self.assertEqual("Free", activity["Price Category"])
        
        self.assertEqual("08:00", details[0]["time"].split("-")[0])
        self.assertEqual("19:00", details[-1]["time"].split("-")[-1])
        
        
        
        #No input for price_category
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = "Cultural & Heritage",
            #price_category = "Free",
            start_time = "0800",
            end_time = "1900"
        )
        itinerary = json.loads(self.itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid["Itineraryid"]))
        
        self.assertEqual(1, itinerary["Userid"])
        self.assertEqual("Unit Testing", itinerary["Title"])
        self.assertEqual("2025-04-10", itinerary["Date"])

        details = json.loads(itinerary["Details"])
        for event in details:
            if "activity" in event.keys():
                activity = json.loads(self.activity_controller.internal_get_activity_by_id(event["id"]))
                self.assertEqual("Cultural & Heritage", activity["Type"])
        
        self.assertEqual("08:00", details[0]["time"].split("-")[0])
        self.assertEqual("19:00", details[-1]["time"].split("-")[-1])
        
        
        
        #No input for start_time
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = "Cultural & Heritage",
            price_category = "Free",
            #start_time = "0800",
            end_time = "1900"
        )
        itinerary = json.loads(self.itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid["Itineraryid"]))
        
        self.assertEqual(1, itinerary["Userid"])
        self.assertEqual("Unit Testing", itinerary["Title"])
        self.assertEqual("2025-04-10", itinerary["Date"])

        details = json.loads(itinerary["Details"])
        for event in details:
            if "activity" in event.keys():
                activity = json.loads(self.activity_controller.internal_get_activity_by_id(event["id"]))
                self.assertEqual("Cultural & Heritage", activity["Type"])
                self.assertEqual("Free", activity["Price Category"])
        
        self.assertEqual("08:00", details[0]["time"].split("-")[0])
        self.assertEqual("19:00", details[-1]["time"].split("-")[-1])
    
    
    
        #No input for end_time
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = "Cultural & Heritage",
            price_category = "Free",
            start_time = "0800"
            #end_time = "1900"
        )
        itinerary = json.loads(self.itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid["Itineraryid"]))
        
        self.assertEqual(1, itinerary["Userid"])
        self.assertEqual("Unit Testing", itinerary["Title"])
        self.assertEqual("2025-04-10", itinerary["Date"])

        details = json.loads(itinerary["Details"])
        for event in details:
            if "activity" in event.keys():
                activity = json.loads(self.activity_controller.internal_get_activity_by_id(event["id"]))
                self.assertEqual("Cultural & Heritage", activity["Type"])
                self.assertEqual("Free", activity["Price Category"])
        
        self.assertEqual("08:00", details[0]["time"].split("-")[0])
        self.assertEqual("19:00", details[-1]["time"].split("-")[-1])
        
        
        
        #price_category=None
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = "Cultural & Heritage",
            price_category = None,
            start_time = "0800",
            end_time = "1900"
        )
        itinerary = json.loads(self.itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid["Itineraryid"]))
        
        self.assertEqual(1, itinerary["Userid"])
        self.assertEqual("Unit Testing", itinerary["Title"])
        self.assertEqual("2025-04-10", itinerary["Date"])

        details = json.loads(itinerary["Details"])
        for event in details:
            if "activity" in event.keys():
                activity = json.loads(self.activity_controller.internal_get_activity_by_id(event["id"]))
                self.assertEqual("Cultural & Heritage", activity["Type"])
        
        self.assertEqual("08:00", details[0]["time"].split("-")[0])
        self.assertEqual("19:00", details[-1]["time"].split("-")[-1])
        
        
        
        #activity_type=None
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = None,
            price_category = "Free",
            start_time = "0800",
            end_time = "1900"
        )
        itinerary = json.loads(self.itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid["Itineraryid"]))
        
        self.assertEqual(1, itinerary["Userid"])
        self.assertEqual("Unit Testing", itinerary["Title"])
        self.assertEqual("2025-04-10", itinerary["Date"])

        details = json.loads(itinerary["Details"])
        for event in details:
            if "activity" in event.keys():
                activity = json.loads(self.activity_controller.internal_get_activity_by_id(event["id"]))
                self.assertEqual("Free", activity["Price Category"])
        
        self.assertEqual("08:00", details[0]["time"].split("-")[0])
        self.assertEqual("19:00", details[-1]["time"].split("-")[-1])
        
        
        
        #activity_type = None, price_category = None
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = None,
            price_category = None,
            start_time = "0800",
            end_time = "1900"
        )
        itinerary = json.loads(self.itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid["Itineraryid"]))
        
        self.assertEqual(1, itinerary["Userid"])
        self.assertEqual("Unit Testing", itinerary["Title"])
        self.assertEqual("2025-04-10", itinerary["Date"])
        
        self.assertEqual("08:00", details[0]["time"].split("-")[0])
        self.assertEqual("19:00", details[-1]["time"].split("-")[-1])
        
        
        
        #activity_type = "Outdoor & Nature", price_category = "$$$" -> len(activities) == 0
        result = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = "Outdoor & Nature",
            price_category = "$$$",
            start_time = "0800",
            end_time = "1900"
        )
        
        self.assertEqual(False, result)
        
        
    def test_internal_share_itinerary(self):
        #Everything valid
        response = self.itinerary_controller.internal_share_itinerary(
            userid = 1,
            itineraryid = 1,
            sharedname = "cccc"
        )
        self.assertEqual(True, response)
        
        
        
        #Invalid itineraryid, does not fufil foreign key requriment
        response = self.itinerary_controller.internal_share_itinerary(
            userid = 1,
            itineraryid = 1,
            sharedname = "xxxx"
        )
        self.assertEqual(False, response)
        
        
    def test_delete_itinerary(self):
        #Test with valid itineraryid
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = "Cultural & Heritage",
            price_category = "Free",
            start_time = "0800",
            end_time = "1900"
        )
        response = self.itinerary_controller.internal_delete_itinerary(1,itineraryid["Itineraryid"])
        self.assertEqual(True, response)
        
        
        #Test with invalid itineraryid
        response = self.itinerary_controller.internal_delete_itinerary(1,1900)
        self.assertEqual(False, response)
    
    
    def test_update_itinerary(self):
        #Test with valid itineraryid
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = "Cultural & Heritage",
            price_category = "Free",
            start_time = "0800",
            end_time = "1900"
        )
        response = self.itinerary_controller.internal_update_itinerary(
            itineraryid=itineraryid["Itineraryid"],
            title = "Unit Testing Updated",
            date = "2025-04-11",
            details = "HIHI"
        )
        self.assertEqual(True, response)
        
        
        #Test with invalid itineraryid
        responsenew = self.itinerary_controller.internal_update_itinerary(
            itineraryid=1900,
            title = "Unit Testing Updated",
            date = "2025-04-11",
            details = "HIHI"
        )
        self.assertEqual(False, responsenew)
        
    
    def test_get_itinerary_by_itineraryid(self):
        itineraryid = self.itinerary_controller.internal_generate_itinerary(
            userid = 1,
            title = "Unit Testing",
            date = "2025-04-10",
            activity_type = "Cultural & Heritage",
            price_category = "Free",
            start_time = "0800",
            end_time = "1900"
        )
        itinerary = json.loads(self.itinerary_controller.internal_get_itinerary_by_itineraryid(itineraryid["Itineraryid"]))
        
        self.assertEqual(1, itinerary["Userid"])
        self.assertEqual("Unit Testing", itinerary["Title"])
        self.assertEqual("2025-04-10", itinerary["Date"])

        details = json.loads(itinerary["Details"])
        for event in details:
            if "activity" in event.keys():
                activity = json.loads(self.activity_controller.internal_get_activity_by_id(event["id"]))
                self.assertEqual("Cultural & Heritage", activity["Type"])
                self.assertEqual("Free", activity["Price Category"])
        
        self.assertEqual("08:00", details[0]["time"].split("-")[0])
        self.assertEqual("19:00", details[-1]["time"].split("-")[-1])
        
        
    def test_get_shared_itineraries(self):
        shareditineraries = self.itinerary_controller.internal_get_shared_itineraries(
            userid = 4
        )
        self.assertNotEqual(None, shareditineraries)


    def test_get_my_itineraries(self):
        myitineraries = self.itinerary_controller.internal_get_my_itineraries(
            userid = 1
        )
        self.assertNotEqual(None, myitineraries)
        
        
if __name__ == "__main__":
    load_dotenv()
    unittest.main() 
    