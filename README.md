# windstatistics
get wind data from fmi.fi and create statistics
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


# Example output: 

# $ python3 tuulistats.py --file LiperiTuiskavanluoto.csv --foil 4 --twin 7 --location 62.6 29.3 --monthly

# Vuositilastot (päivän maksimi >= raja-arvo):
# Foilikeli >= 4.0 m/s, Twinikeli >= 7.0 m/s
# ---------------------------------------------------------------
# 2020 | Foilikeli: 303 | Twinikeli: 219
# 2021 | Foilikeli: 274 | Twinikeli: 192
# 2022 | Foilikeli: 280 | Twinikeli: 179
# 2023 | Foilikeli: 128 | Twinikeli: 79
# 2025 | Foilikeli: 201 | Twinikeli: 132
# 
# Kuukausittaiset tilastot:
# Vuosi-Kk | Foilikeli | Twinikeli
# --------------------------------
# 2020-01 | 30 | 23
# 2020-02 | 28 | 22
# 2020-03 | 31 | 27
2020-04 | 30 | 24
2020-05 | 23 | 14
