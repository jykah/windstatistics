
#!/usr/bin/env python3
import pandas as pd
from astral import LocationInfo
from astral.sun import sun
import pytz
import argparse

# Argumentit
parser = argparse.ArgumentParser(description="Laskee tuulistatsit valoisan ajan perusteella.")
parser.add_argument("--file", type=str, required=True, help="CSV-tiedoston polku")
parser.add_argument("--direction", nargs=2, type=int, help="Tuulen suuntaväli (esim. 170 240)")
parser.add_argument("--foil", type=float, default=6.0, help="Foilikeli raja-arvo (m/s)")
parser.add_argument("--twin", type=float, default=9.0, help="Twinikeli raja-arvo (m/s)")
parser.add_argument("--location", nargs=2, type=float, default=[59.83, 22.97],
                    help="Sijainnin koordinaatit (lat lon), oletus Hanko/Tulliniemi")
parser.add_argument("--monthly", action="store_true", help="Näytä myös kuukausittaiset tilastot")
args = parser.parse_args()

file_path = args.file
direction_range = args.direction
foil_threshold = args.foil
twin_threshold = args.twin
lat, lon = args.location

# Lue CSV
df = pd.read_csv(file_path)

# Muodosta datetime-sarake ja lisää aikavyöhyke (käsitellään DST-ongelmat)
df["datetime"] = pd.to_datetime(
    df["Vuosi"].astype(str) + "-" +
    df["Kuukausi"].astype(str) + "-" +
    df["Päivä"].astype(str) + " " +
    df["Aika [Paikallinen aika]"]
).dt.tz_localize("Europe/Helsinki", ambiguous="NaT", nonexistent="shift_forward")

# Poista rivit, joissa aika jäi epäselväksi
df = df.dropna(subset=["datetime"])

df["date"] = df["datetime"].dt.date
df["year"] = df["datetime"].dt.year
df["month"] = df["datetime"].dt.month

# Muunna nopeus ja suunta numeroksi, ohita virheelliset arvot
df["speed"] = pd.to_numeric(df["Keskituulen nopeus [m/s]"], errors="coerce")
df["direction"] = pd.to_numeric(df["Tuulen suunta [°]"], errors="coerce")
df = df.dropna(subset=["speed", "direction"])

# Astral: sijainti käyttäjän antamilla koordinaateilla
location = LocationInfo("Custom", "Finland", "Europe/Helsinki", lat, lon)
tz = pytz.timezone("Europe/Helsinki")

# Suodata valoisan ajan havainnot (ja suunta, jos annettu)
daylight_rows = []
for idx, row in df.iterrows():
    try:
        s = sun(location.observer, date=row["date"], tzinfo=tz)
        sunrise = s.get("sunrise")
        sunset = s.get("sunset")
        if sunrise and sunset and sunrise <= row["datetime"] <= sunset:
            if direction_range:
                if direction_range[0] <= row["direction"] <= direction_range[1]:
                    daylight_rows.append(row)
            else:
                daylight_rows.append(row)
    except ValueError:
        continue  # Kaamospäivä

filtered_df = pd.DataFrame(daylight_rows)

# Ryhmittele päivittäin ja etsi maksimi tuulen nopeus
daily_max = filtered_df.groupby(["year", "month", "date"])["speed"].max()

# Vuosittaiset tilastot
summary_year = daily_max.groupby("year").agg(
    Foilikeli_päiviä=lambda x: (x >= foil_threshold).sum(),
    Twinikeli_päiviä=lambda x: (x >= twin_threshold).sum()
)

print(f"\nVuositilastot (päivän maksimi >= raja-arvo):")
print(f"Foilikeli >= {foil_threshold} m/s, Twinikeli >= {twin_threshold} m/s")
print("---------------------------------------------------------------")
for year, row in summary_year.iterrows():
    print(f"{year} | Foilikeli: {row['Foilikeli_päiviä']} | Twinikeli: {row['Twinikeli_päiviä']}")

# Kuukausittaiset tilastot (jos pyydetty)
if args.monthly:
    print(f"\nKuukausittaiset tilastot:")
    print("Vuosi-Kk | Foilikeli | Twinikeli")
    print("--------------------------------")
    summary_month = daily_max.groupby(["year", "month"]).agg(
        Foilikeli_päiviä=lambda x: (x >= foil_threshold).sum(),
        Twinikeli_päiviä=lambda x: (x >= twin_threshold).sum()
    )
    for (year, month), row in summary_month.iterrows():
        print(f"{year}-{month:02d} | {row['Foilikeli_päiviä']} | {row['Twinikeli_päiviä']}")

# ---------------------------------------------------------------
# ESIMERKKI KÄYTÖSTÄ:
# Vuosittaiset statsit:
#   python3 tuulistats.py --file LiperiTuiskavanluoto.csv
#
# Vuosittaiset + kuukausittaiset statsit:
#   python3 tuulistats.py --file LiperiTuiskavanluoto.csv --monthly
#
# Suuntaväli:
#   python3 tuulistats.py --file LiperiTuiskavanluoto.csv --direction 170 240
#
# Muuta raja-arvoja:
#   python3 tuulistats.py --file LiperiTuiskavanluoto.csv --foil 4 --twin 7
#
# Vaihda sijainti Liperiin:
#   python3 tuulistats.py --file LiperiTuiskavanluoto.csv --location 62.6 29.3
# ---------------------------------------------------------------
# https://www.ilmatieteenlaitos.fi/havaintojen-lataus csv:t voi hakea täältä (toimii huonosti)
