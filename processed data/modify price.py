import pandas as pd

activites_df = pd.read_csv("All_Data.csv", delimiter="\t", on_bad_lines='warn')

rows = activites_df.shape[0] #Number of rows

# Function to extract and compute the average price
def extract_avg_price(price_str):
    if 'to' in price_str:
        # Extract the numerical values from the string (e.g., "$10.00 to $20.00" -> (10.00, 20.00))
        price_range = price_str.lower().strip("from").split(' to ')
        start = float(price_range[0].replace('$', '').strip())
        end = float(price_range[1].replace('$', '').strip())
        return "~"+str(round((start + end) / 2, 1))  # Return the average of the two prices
    return str(float(price_str.strip("$").replace(",", "")))  # If no 'to', return the original string

# Function to categorize the price
def categorize_price(price):
    price = float(price.strip("~"))
    if price == 0:
        return 'Free'
    elif price <= 50:
        return '$'
    elif 50 < price <= 100:
        return '$$'
    else:
        return '$$$'
    
# Apply the function to replace the "Price" column with average price
activites_df['Price'] = activites_df['Price'].apply(extract_avg_price)

# Add the new column for price categories
activites_df['Price Category'] = activites_df['Price'].apply(categorize_price)

activites_df.to_csv('updated_prices.csv')
