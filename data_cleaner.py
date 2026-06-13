import pandas as pd


def clean_car_data():
    print("Loading raw data...")
    df = pd.read_csv("raw_cars_data.csv")

    # 1. URL-ek javítása (ahogy eddig is)
    base_url = "https://www.hasznaltauto.hu"
    df['Link'] = df['Link'].apply(lambda x: base_url + x if not str(x).startswith('http') else x)

    # 2. Ár (Price) tisztítása
    print("Cleaning Price column...")
    df['Price_Clean'] = df['Price'].str.replace(r'\D', '', regex=True)
    df['Price_Clean'] = pd.to_numeric(df['Price_Clean'], errors='coerce')

    # --- SPRINT 2.2: DEEP FEATURE ENGINEERING ---
    print("Extracting features from Tech_Data...")

    # Biztosítjuk, hogy szövegként kezelje az oszlopot
    tech_col = df['Tech_Data'].astype(str)

    # ÜZEMANYAG (Fuel): Feltételezzük, hogy az első szó a vessző előtt
    df['Fuel'] = tech_col.str.split(',').str[0].str.strip()

    # ÉVJÁRAT (Year): Keresünk pontosan 4 darab számjegyet: \d{4}
    df['Year'] = tech_col.str.extract(r'(\d{4})')[0]
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    # MOTOR ŰRTARTALOM (Engine_cm3): Számok (\d) és szóközök (\s), amik után "cm³" jön
    # A nyers kinyerés után egyből le is takarítjuk róla a betűket a str.replace-szel
    df['Engine_cm3'] = tech_col.str.extract(r'([\d\s\xa0]+)\s*cm³')[0].str.replace(r'\D', '', regex=True)
    df['Engine_cm3'] = pd.to_numeric(df['Engine_cm3'], errors='coerce')

    # TELJESÍTMÉNY (Power_LE): Számok és szóközök, amik után "LE" jön
    df['Power_LE'] = tech_col.str.extract(r'([\d\s\xa0]+)\s*LE')[0].str.replace(r'\D', '', regex=True)
    df['Power_LE'] = pd.to_numeric(df['Power_LE'], errors='coerce')

    # FUTÁSTELJESÍTMÉNY (Mileage_km): Számok és szóközök, amik után "km" jön
    df['Mileage_km'] = tech_col.str.extract(r'([\d\s\xa0]+)\s*km')[0].str.replace(r'\D', '', regex=True)
    df['Mileage_km'] = pd.to_numeric(df['Mileage_km'], errors='coerce')

    # 3. Felesleges, nyers oszlopok eldobása (Opcionális, de szebb lesz tőle az adatbázis)
    # A 'Price' és a 'Tech_Data' már be lettek dolgozva, nincs rájuk szükség
    df = df.drop(columns=['Price', 'Tech_Data'])

    print("\n--- FINAL CLEANED DATA ---")
    print(df.head())
    print("\nFinal data types:\n", df.dtypes)

    # Export
    df.to_csv("cleaned_cars_data.csv", index=False, encoding='utf-8')
    print("\nCleaned data saved to 'cleaned_cars_data.csv'.")


if __name__ == "__main__":
    clean_car_data()