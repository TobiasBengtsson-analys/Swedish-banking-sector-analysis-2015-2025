import pandas as pd


# På grund av begränsning i antal celler tillåtna från SCB laddas datan in igen med endast rätta variabler för att få ett större dataset

Data_komplett = pd.read_csv("data/Data_komplett.csv",
                   encoding = 'latin1',
                   sep = ",")

Data_komplett = pd.DataFrame(Data_komplett)

Data_komplett["institut"] = Data_komplett["institut"].replace(
    {"Skandinaviska Enskilda Banken AB (Publ)": "SEB",
    "Svenska Handelsbanken AB (Publ)": "Handelsbanken",
    "Swedbank AB (Publ)": "Swedbank"}
)


# Flytta ner kontoposter till en egen kolumn

Data_komplett = Data_komplett.melt(
    id_vars = ["månad", "institut"],
    var_name = "kontopost",
    value_name = "värde"
)

Data_komplett["månad"] = pd.to_datetime(
    Data_komplett["månad"].str.replace("M", "-"),
    format="%Y-%m"
)

Data_komplett.to_csv("data/Data_processed.csv", index=False)
