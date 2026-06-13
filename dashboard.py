import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Oldal beállításai
st.set_page_config(page_title="Twingo Market Analytics", layout="wide")
st.title("🚗 Renault Twingo Piaci Elemző Dashboard")
st.markdown("Interaktív adatelemzés a Használtautó.hu adatai alapján.")

# 2. Adatbetöltés (Cacheljük, hogy gyors legyen a weboldal)
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_cars_data.csv")

df = load_data()

# 3. Oldalsáv (Sidebar) - Interaktív szűrők
st.sidebar.header("⚙️ Szűrők")

# Évjárat csúszka
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
selected_years = st.sidebar.slider("Gyártási év", min_year, max_year, (min_year, max_year))

# Motor méret szűrő
engines = df['Engine_cm3'].dropna().unique().tolist()
engines.sort()
selected_engines = st.sidebar.multiselect("Motor űrtartalom (cm³)", engines, default=engines)

# 4. Az adatok szűrése a felhasználó beállításai alapján
filtered_df = df[
    (df['Year'] >= selected_years[0]) &
    (df['Year'] <= selected_years[1]) &
    (df['Engine_cm3'].isin(selected_engines))
]

# 5. Interaktív Plotly Grafikon
st.subheader(f"Ár és Futásteljesítmény ({len(filtered_df)} db autó)")

fig = px.scatter(
    filtered_df,
    x="Mileage_km",
    y="Price_Clean",
    color="Year",          # Színkódolás évjárat alapján
    hover_data=["Title", "Engine_cm3", "Link"], # Egeret ráhúzva ezeket mutatja
    labels={
        "Mileage_km": "Futásteljesítmény (km)",
        "Price_Clean": "Ár (HUF)",
        "Year": "Évjárat"
    },
    template="plotly_white"
)

# A grafikon megjelenítése a weblapon
st.plotly_chart(fig, use_container_width=True)

# 6. Nyers adatok mutatása (opcionális)
if st.checkbox("Nyers adatok megjelenítése (Táblázat)"):
    st.dataframe(filtered_df)