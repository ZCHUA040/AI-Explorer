import sqlite3
import pandas as pd


conn = sqlite3.connect("../test.db")

activites_df = pd.read_csv("All_Data.csv", delimiter="\t", on_bad_lines='warn')

rows = activites_df.shape[0] #Number of rows

for i in range(rows):
    name = activites_df["Name"][i]
    type = activites_df["Type"][i]
    location = activites_df["Location"][i]
    price = activites_df["Price"][i]

    conn.execute(
                 "INSERT INTO Activities (Name, Type, Location, Price) VALUES (?, ?, ?, ?)",
                 (name, type, location, price)
                 )
    conn.commit()

conn.close()
        
    