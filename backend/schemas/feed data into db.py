import sqlite3
import pandas as pd


conn = sqlite3.connect("../test.db")

activites_df = pd.read_csv("All_Data_v2.csv", on_bad_lines='warn')

rows = activites_df.shape[0] #Number of rows
print(rows)
for i in range(rows):
    name = activites_df["Name"][i]
    type = activites_df["Type"][i]
    location = activites_df["Location"][i]
    price = activites_df["Price"][i]
    price_cat = activites_df["Price Category"][i]
    cursor = conn.cursor()
    cursor.execute(
                 "INSERT INTO Activities (Name, Type, Location, Price, Price_Category) VALUES (?, ?, ?, ?, ?)",
                 (name, type, location, price, price_cat)
                 )
    conn.commit()

conn.close()
        
    