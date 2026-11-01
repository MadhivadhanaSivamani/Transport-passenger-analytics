
import os
import requests
import pandas as pd

API_URL = "https://data.cityofchicago.org/resource/jyb9-n7fm.csv"

os.makedirs("data", exist_ok=True)

print("Downloading passenger dataset...")

params = {
    "$limit": 500000,
    "$order": "date ASC"
}

try:
    response = requests.get(
        API_URL,
        params=params,
        timeout=120
    )

    response.raise_for_status()

    with open("data/cta_ridership.csv", "wb") as f:
        f.write(response.content)

    df = pd.read_csv("data/cta_ridership.csv")

    print("Dataset downloaded successfully!")
    print("Total records:", len(df))
    print("Columns:", df.columns.tolist())
    print(df.head())

except Exception as e:
    print("Error:", e)
