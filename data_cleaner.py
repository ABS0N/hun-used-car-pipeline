import pandas as pd
import numpy as np


def clean_car_data():
    print("Loading raw data...")
    # 1. Beolvassuk az előzőleg lementett CSV fájlt
    df = pd.read_csv("raw_cars_data.csv")

    print("\n--- BEFORE CLEANING (Data Types) ---")
    print(df.dtypes)  # Ez megmutatja, hogy jelenleg minden 'object' (vagyis string)

    # 2. Az Ár (Price) oszlop megtisztítása
    print("\nCleaning Price column...")

    # LÉPÉS A: Regex használata.
    # A \D jelentése: "minden, ami NEM számjegy". Ezt lecseréljük semmire ('').
    # A regex=True bekapcsolja a reguláris kifejezések értelmezését.
    df['Price_Clean'] = df['Price'].str.replace(r'\D', '', regex=True)

    # LÉPÉS B: Típuskonverzió (String-ből Numerikus formátumba)
    # A pd.to_numeric megpróbálja számmá alakítani az oszlopot.
    # Az errors='coerce' a varázsszó: ha valami üres maradt (pl. a "Kérjen ajánlatot"
    # miatt nem maradt számjegy), azt nem dobja hibára, hanem betesz egy NaN-t (Not a Number).
    df['Price_Clean'] = pd.to_numeric(df['Price_Clean'], errors='coerce')

    print("\n--- AFTER CLEANING ---")
    # Megnézzük az eredeti és a tisztított oszlopot egymás mellett
    print(df[['Price', 'Price_Clean']].head(10))
    print(f"\nNew data types:\n{df.dtypes}")

    # 3. Exportáljuk a már elemzésre kész adatbázist
    df.to_csv("cleaned_cars_data.csv", index=False, encoding='utf-8')
    print("\nCleaned data saved to 'cleaned_cars_data.csv'.")


if __name__ == "__main__":
    clean_car_data()