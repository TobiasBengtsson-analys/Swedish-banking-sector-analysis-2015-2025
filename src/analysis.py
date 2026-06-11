import pandas as pd
import numpy as np

def calculate_cagr(start_value, end_value, n_years):
    """Beräknar Compound Annual Growth Rate (CAGR)."""
    if start_value <= 0 or end_value <= 0:
        return np.nan
    return (end_value / start_value) ** (1 / n_years) - 1

def main():
    # 1. Läs in den städade datan
    try:
        df = pd.read_csv("data/Data_processed.csv")
    except FileNotFoundError:
        print("Fel: Hittade inte data/Data_processed.csv. Kör data_cleaning.py först.")
        return

    # Säkerställ att månad är i datetime-format
    df["månad"] = pd.to_datetime(df["månad"])

    print("=" * 60)
    print("ANALYS AV SVENSKA STORBANKERS BALANSRÄKNINGAR")
    print("=" * 60)

    # ---------------------------------------------------------
    # 2. ANALYS: TOTALA TILLGÅNGAR
    # ---------------------------------------------------------
    print("\n--- 2. Totala tillgångar ---")
    tillgangar = df[df["kontopost"] == "120 Summa tillgångar"]
    tillgangar_per_manad = tillgangar.groupby("månad")["värde"].sum() / 1000  # Till miljarder SEK

    assets_start_2015 = tillgangar_per_manad.loc[pd.Timestamp('2015-12-01')]
    assets_start_2020 = tillgangar_per_manad.loc[pd.Timestamp('2020-12-01')]
    assets_end_2025   = tillgangar_per_manad.loc[pd.Timestamp('2025-12-01')]

    cagr_assets_15_25 = calculate_cagr(assets_start_2015, assets_end_2025, 10)
    cagr_assets_20_25 = calculate_cagr(assets_start_2020, assets_end_2025, 5)

    print(f"Totala tillgångar vid utgången av 2025: {assets_end_2025.round().astype(int)} mdr SEK")
    print(f"Genomsnittlig årlig tillväxt (CAGR) 2015–2025: {cagr_assets_15_25 * 100:.2f} %")
    print(f"Genomsnittlig årlig tillväxt (CAGR) 2020–2025: {cagr_assets_20_25 * 100:.2f} %")

    # ---------------------------------------------------------
    # 3. ANALYS: TOTAL UTLÅNING
    # ---------------------------------------------------------
    print("\n--- 3. Total utlåning ---")
    utlaning = df[df["kontopost"] == "103 Utlåning, Totalt"]
    utlaning_per_manad = utlaning.groupby("månad")["värde"].sum() / 1000  # Till miljarder SEK

    lending_start_2015 = utlaning_per_manad.loc[pd.Timestamp('2015-12-01')]
    lending_start_2020 = utlaning_per_manad.loc[pd.Timestamp('2020-12-01')]
    lending_end_2025   = utlaning_per_manad.loc[pd.Timestamp('2025-12-01')]

    cagr_lending_15_25 = calculate_cagr(lending_start_2015, lending_end_2025, 10)
    cagr_lending_20_25 = calculate_cagr(lending_start_2020, lending_end_2025, 5)

    print(f"Total utlåning vid utgången av 2025: {lending_end_2025.round().astype(int)} mdr SEK")
    print(f"Genomsnittlig årlig tillväxt (CAGR) 2015–2025: {cagr_lending_15_25 * 100:.2f} %")
    print(f"Genomsnittlig årlig tillväxt (CAGR) 2020–2025: {cagr_lending_20_25 * 100:.2f} %")

    # ---------------------------------------------------------
    # 4. ANALYS: FINANSIERING & KATEGORIER
    # ---------------------------------------------------------
    print("\n--- 4. Finansieringsstruktur ---")

    # Filtrera och harmonisera kategorier på en kopia för att undvika varningar
    finansiering = df[df["kontopost"].isin([
        "201 In-/upplåning, Totalt",
        "203 Emitterade värdepapper",
        "2035 Säkerställda obligationer, Emitterade"
    ])].copy()

    finansiering["kontopost"] = finansiering["kontopost"].replace({
        "201 In-/upplåning, Totalt": "In-/upplåning",
        "203 Emitterade värdepapper": "Emitterade värdepapper",
        "2035 Säkerställda obligationer, Emitterade": "Emitterade värdepapper"
    })

    # Aggregera per månad och kontopost (miljarder SEK)
    finansiering_per_manad = finansiering.groupby(["månad", "kontopost"])["värde"].sum() / 1000

    # Beräkna CAGR per kategori
    for kat in ["In-/upplåning", "Emitterade värdepapper"]:
        fin_start_2015 = finansiering_per_manad.loc[(pd.Timestamp('2015-12-01'), kat)]
        fin_start_2020 = finansiering_per_manad.loc[(pd.Timestamp('2020-12-01'), kat)]
        fin_end_2025   = finansiering_per_manad.loc[(pd.Timestamp('2025-12-01'), kat)]

        cagr_fin_15_25 = calculate_cagr(fin_start_2015, fin_end_2025, 10)
        cagr_fin_20_25 = calculate_cagr(fin_start_2020, fin_end_2025, 5)

        print(f"{kat}:")
        print(f"  Totalt 2025: {fin_end_2025:.0f} mdr SEK")
        print(f"  CAGR 2015–2025: {cagr_fin_15_25 * 100:.2f} %")
        print(f"  CAGR 2020–2025: {cagr_fin_20_25 * 100:.2f} %")

    # ---------------------------------------------------------
    # 5. ANALYS: STRUKTURELLA ANDELAR OCH NYCKELTAL (DECEMBER 2025)
    # ---------------------------------------------------------
    print("\n--- 5. Strukturella nyckeltal (December 2025) ---")

    # Förbered data för december 2025 på banknivå
    df_2025 = df[df["månad"] == pd.Timestamp("2025-12-01")].copy()

    # Pivotera för att få variablerna som egna kolumner per institut
    df_pivot = df_2025.pivot(index="institut", columns="kontopost", values="värde")

    # Slå samman Säkerställda och Emitterade till en total marknadsfinansiering
    df_pivot["Marknadsfinansiering"] = df_pivot["203 Emitterade värdepapper"].fillna(0) + df_pivot["2035 Säkerställda obligationer, Emitterade"].fillna(0)
    df_pivot = df_pivot.rename(columns={
        "120 Summa tillgångar": "Tillgångar",
        "103 Utlåning, Totalt": "Utlåning",
        "201 In-/upplåning, Totalt": "In_Upplåning"
    })

    # Beräkna individuella kvoter
    df_pivot["Andel_In_Upplåning"] = (df_pivot["In_Upplåning"] / (df_pivot["In_Upplåning"] + df_pivot["Marknadsfinansiering"])) * 100
    df_pivot["Andel_Marknad"] = 100 - df_pivot["Andel_In_Upplåning"]
    df_pivot["LTA"] = (df_pivot["Utlåning"] / df_pivot["Tillgångar"]) * 100
    df_pivot["LTD"] = (df_pivot["Utlåning"] / df_pivot["In_Upplåning"]) * 100

    # Skriv ut genomsnitt för systemet (storbankerna aggregerat)
    print(f"Genomsnittlig andel In-/upplåning: {df_pivot['Andel_In_Upplåning'].mean().round()}%")
    print(f"Genomsnittlig andel Emitterade värdepapper: {df_pivot['Andel_Marknad'].mean().round()}%")
    print(f"Genomsnittlig Utlånings-/tillgångskvot (LTA): {df_pivot['LTA'].mean().round()}%")
    print(f"Genomsnittlig System-LTD-kvot: {df_pivot['LTD'].mean().round()}%")

    print("\nNyckeltal uppdelat per institut för december 2025:")
    print(df_pivot[["LTA", "LTD", "Andel_In_Upplåning", "Andel_Marknad"]].round(1))
    print("=" * 60)

if __name__ == "__main__":
    main()
