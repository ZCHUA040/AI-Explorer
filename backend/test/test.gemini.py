import google.generativeai as genai
import os
import re
import json
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "models/gemini-2.0-flash"


def extract_itinerary_details(text):
    """
    Extracts structured itinerary details from the AI response.
    """
    itinerary = []
    events = text.split("\n\n")  # Split by double newlines for each event block

    time_pattern = re.compile(r"\*{0,2}\s*(\d{1,2}:\d{2} [APM]{2}) - (\d{1,2}:\d{2} [APM]{2})\s*\*{0,2}")  # Match time blocks
    location_pattern = re.compile(r"\*\*Location:\*\* (.+)")  # Extract locations explicitly mentioned

    known_places = [
        "Lau Pa Sat", "Amoy Street Food Centre", "National Museum of Singapore",
        "Fort Canning Park", "Peranakan Museum", "Dhoby Ghaut MRT", "Plaza Singapura"
    ]

    for event in events:
        match = time_pattern.search(event)
        if match:
            start_time, end_time = match.groups()
            lines = event.split("\n")
            title = lines[0].strip("* ").strip()
            details = " ".join(lines[1:]).strip()
            location = None

            # **1️⃣ First: Try explicit "Location" extraction**
            location_match = location_pattern.search(details)
            if location_match:
                location = location_match.group(1)

            # **2️⃣ If no explicit location, check for known place names**
            if not location:
                for place in known_places:
                    if place in details:
                        location = place
                        break

            # **3️⃣ If still no location, check if title contains a place**
            if not location:
                for place in known_places:
                    if place in title:
                        location = place
                        break

            itinerary.append({
                "start_time": start_time,
                "end_time": end_time,
                "title": title,
                "description": details,
                "location": location if location else "Unknown"
            })

    return itinerary


def generate_itinerary(time, date, budget, location, interests):
    """
    Generate an AI-powered itinerary and return structured JSON.
    """
    prompt = f"""
    I am planning a day out in Singapore between {time} and in the area of {location}.
    My interests are: {', '.join(interests)}.
    My available dates are: {date}.
    My budget is: {budget}.
    Please suggest a detailed itinerary with activities, food options, and must-see places.
    """

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        structured_itinerary = extract_itinerary_details(response.text)
        return json.dumps({"itinerary": structured_itinerary}, indent=4) if structured_itinerary else json.dumps({"error": "No structured itinerary found"})

    except Exception as e:
        return json.dumps({"error": f"API Error: {e}"})


# **TEST CASE**
print("\n AI-Generated Itinerary in JSON Format:")
print(generate_itinerary("8:30 AM to 4:30 PM", "17/03/2025", "$50", "Central", ["Museums", "Food", "Historical Sites"]))
