import google.generativeai as genai
import sqlite3
import os
import random, json

# Configure Gemini API
genai.configure(api_key="")

# Define the activities list
conn = sqlite3.connect("test.db")
activities = conn.execute("SELECT Activityid, NAME FROM Activities WHERE Price_Category = ?", ("$",)).fetchall()
random.shuffle(activities)

start_time = "0800"
end_time = "2100"
# Prompt for the Gemini model
prompt = f"""
Create a detailed itinerary for a single day from {start_time} to {end_time} based on the following activities:
- Have different type of activity of each slot
- Each activity takes 2 hours.
- Travel time between activities is 1 hour.
- Lunch should be scheduled for 2 hours. (Only if start time is before noon)
- Lunch must occur at 1100 or 1200 or 1300.
- You need to travel to and from lunch.
- If there is less than 2 hours left, end itinerary.
- Put the activity id beside the timeslot
- Ensure a logical sequence.

List of activities with their id:
{activities}

Output the itinerary in a structured json format with timeslots, do not include anything else.
Sample output {{"time": "0800-1200", "id":1, "activity":"Swimming"}}
"""

# Generate response
model = genai.GenerativeModel("models/gemini-2.0-flash")
response = model.generate_content(prompt)

# Print itinerary
print(response.text)
json_itinerary = json.loads(response.text.strip("`").strip("json"))
print(json_itinerary)
