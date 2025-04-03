import sqlite3
import pandas as pd
import google.generativeai as genai
import sqlite3
import os
import random, json
from dotenv import load_dotenv
import requests
from time import sleep 

load_dotenv()


import google.generativeai as genai
import os
import urllib.parse

def get_google_maps_iframe(address):
    """Generates an iframe code for embedding a Google Maps location without using an API key."""
    # URL encode the address to make it safe for use in the URL
    encoded_address = urllib.parse.quote(address)
    
    # Construct the iframe URL for a simple embed (without requiring an API key)
    iframe_url = f"https://www.google.com/maps?q={encoded_address}&output=embed"
    
    # Generate the iframe HTML code
    #iframe_code = f'<iframe src="{iframe_url}" width="600" height="450" frameborder="0" style="border:0" allowfullscreen></iframe>'
    
    return iframe_url

def get_gemini_description(name, address, category):
    """Retrieves a description from Gemini."""
    genai.configure(api_key="AIzaSyAGrigR7WqmIUSLZ8TTk28cFmUsRROd5Wc")
    prompt = f"""
    Give me a 200 word description of the {name} at {address}, from category {category}.
    - for locations that is a school, assume that it serves as a sports field
    """
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    while True:
        try:
            response = model.generate_content(prompt)
            sleep(1)
            if response.text:
                return response.text
            else:
                return "Gemini did not provide a description."
        except Exception as e:
            if "429" in str(e):
                print("Sleeping")
                sleep(15)
            else:
                return e

conn = sqlite3.connect("test.db")

activites_df = pd.read_csv("All_Data_v2.csv", on_bad_lines='warn')

rows = activites_df.shape[0] #Number of rows

for i in range(1483, rows):
    name = activites_df["Name"][i]
    type = activites_df["Type"][i]
    location = activites_df["Location"][i]
    price = activites_df["Price"][i]
    price_cat = activites_df["Price Category"][i]
    image_url = get_google_maps_iframe(location)
    description = get_gemini_description(name, location, type)
    print(f"Executing row {i}, {name}, {description[:20]}")
    if "sorry" in description.lower() or "unfortunately" in description.lower() or "apologize" in description.lower() or "cannot" in description.lower():
        pass
    else:
        cursor = conn.cursor()
        cursor.execute(
                    "INSERT INTO Activities (Name, Type, Location, Price, Price_Category, Image, Description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name, type, location, price, price_cat, image_url, description)
                    )
        conn.commit()

conn.close()
        
    