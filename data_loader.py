import pandas as pd
import sqlite3

# Step 1: Load the CSV
# We use encoding='latin1' because Superstore CSVs often have special characters
# (like é, ñ) that fail with the default utf-8 encoding
df = pd.read_csv("data/superstore.csv", encoding="latin1")

# Step 2: Clean column names
# SQL doesn't like spaces or special characters in column names
# This converts "Order ID" -> "Order_ID", "Sub-Category" -> "Sub_Category"
df.columns = [col.strip().replace(" ", "_").replace("-", "_") for col in df.columns]

# Step 3: Convert date columns to proper datetime format
# This ensures forecasting and date filtering work correctly later
df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%m/%d/%Y")
df["Ship_Date"] = pd.to_datetime(df["Ship_Date"], format="%m/%d/%Y")

# Step 4: Create SQLite database and load the data
conn = sqlite3.connect("superstore.db")
df.to_sql("orders", conn, if_exists="replace", index=False)
conn.close()

# Step 5: Confirm it worked
print(f"✅ Database created successfully!")
print(f"✅ Total rows loaded: {len(df)}")
print(f"✅ Columns: {list(df.columns)}")