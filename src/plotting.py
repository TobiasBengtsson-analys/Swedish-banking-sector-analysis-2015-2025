import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import os

def main():
    # 1. Säkerställ att mappen 'figures' existerar
    if not os.path.exists("figures"):
        os.makedirs("figures")

    # 2. Läs in den städade datan
    try:
        df = pd.read_csv("data/Data_processed.csv")
    except FileNotFoundError:
        print("Fel: Hittade inte data/Data_processed.csv. Kör data_cleaning.py först.")
        return

    df["månad"] = pd.to_datetime(df["månad"])

    # Gemensamma färgpaletter för konsistens
    bank_colors = {"Handelsbanken": "tab:green", "SEB": "tab:blue", "Swedbank": "tab:orange"}
    ratio_color = "tab:orange"

    print("Genererar grafer...")

    # =========================================================================
    # FIGUR 1: TOTALA TILLGÅNGAR
    # =========================================================================
    tillgangar = df[df["kontopost"] == "120 Summa tillgångar"].copy()
    tillgangar["värde"] = tillgangar["värde"] / 1000  # Till miljarder SEK

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=tillgangar, x="månad", y="värde", hue="institut", palette=bank_colors, ax=ax)

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_ylim(0, 4000)
    ax.set_xlim(pd.Timestamp('2015-01-01'), pd.Timestamp('2025-12-01'))

    plt.title("Svenska storbankers totala tillgångar", fontweight='bold', pad=15)
    plt.ylabel("Miljarder SEK", fontweight='bold')
    plt.xlabel("Tid", fontweight='bold')
    plt.xticks(rotation=45, fontweight='bold')
    plt.yticks(fontweight='bold')

    ax.legend(title=" ", loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)
    plt.tight_layout()
    plt.savefig('figures/Summa_tillgangar.png', dpi=300, facecolor="white")
    plt.close()

    # =========================================================================
    # FIGUR 2: TOTAL UTLÅNING
    # =========================================================================
    utlaning = df[df["kontopost"] == "103 Utlåning, Totalt"].copy()
    utlaning["värde"] = utlaning["värde"] / 1000  # Till miljarder SEK

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=utlaning, x="månad", y="värde", hue="institut", palette=bank_colors, ax=ax)

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_ylim(0, 3000)
    ax.set_xlim(pd.Timestamp('2015-01-01'), pd.Timestamp('2025-12-01'))

    plt.title("Svenska storbankers totala utlåning", fontweight='bold', pad=15)
    plt.ylabel("Miljarder SEK", fontweight='bold')
    plt.xlabel("Tid", fontweight='bold')
    plt.xticks(rotation=45, fontweight='bold')
    plt.yticks(fontweight='bold')

    ax.legend(title=" ", loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)
    plt.tight_layout()
    plt.savefig('figures/Utlaning.png', dpi=300, facecolor="white")
    plt.close()

    # =========================================================================
    # FIGUR 3: FINANSIERING ÖVER TID
    # =========================================================================
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

    finansiering = finansiering.groupby(["månad", "institut", "kontopost"], as_index=False)["värde"].sum()
    finansiering["värde"] = finansiering["värde"] / 1000

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=finansiering, x="månad", y="värde", hue="institut", style="kontopost",
        palette=bank_colors, dashes={"In-/upplåning": "", "Emitterade värdepapper": (5, 5)}, ax=ax
    )

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_xlim(pd.Timestamp('2015-01-01'), pd.Timestamp('2025-12-01'))
    ax.set_ylim(0, 2500)

    plt.title("Svenska storbankers finansiering över tid", fontweight='bold', pad=15)
    plt.ylabel("Miljarder SEK", fontweight='bold')
    plt.xlabel("År", fontweight='bold')
    plt.xticks(rotation=45, fontweight='bold')
    plt.yticks(fontweight='bold')

    # Filtrera bort de automatiska rubrikerna "institut" och "kontopost" från legenden
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles=[h for i, h in enumerate(handles) if labels[i] not in ["institut", "kontopost"]],
        labels=[l for l in labels if l not in ["institut", "kontopost"]],
        loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False
    )
    plt.tight_layout()
    plt.savefig('figures/Finansiering_tid.png', dpi=300, facecolor="white")
    plt.close()

    # Förbered data för december 2025 för figurerna 4, 5 och 6
    df_2025 = df[df["månad"] == pd.Timestamp("2025-12-01")].copy()
    df_pivot = df_2025.pivot(index="institut", columns="kontopost", values="värde")
    df_pivot["Marknadsfinansiering"] = df_pivot["203 Emitterade värdepapper"].fillna(0) + df_pivot["2035 Säkerställda obligationer, Emitterade"].fillna(0)

    # =========================================================================
    # FIGUR 4: FINANSIERINGSSTRUKTUR (STRECKAD/STACKED BAR) 2025
    # =========================================================================
    total_fin = df_pivot["201 In-/upplåning, Totalt"] + df_pivot["Marknadsfinansiering"]
    fin_andel = pd.DataFrame(index=df_pivot.index)
    fin_andel["Andel in-/upplåning"] = (df_pivot["201 In-/upplåning, Totalt"] / total_fin) * 100
    fin_andel["Andel emitterade värdepapper"] = (df_pivot["Marknadsfinansiering"] / total_fin) * 100

    ax = fin_andel.plot(kind="bar", stacked=True, figsize=(6, 5), color=["tab:blue", "tab:orange"])
    ax.set_title("Storbankers finansieringsstruktur\nper december 2025", fontweight='bold', pad=10)
    ax.set_ylabel("Procent", fontweight='bold')
    ax.set_xlabel(" ")
    ax.set_xticklabels(fin_andel.index, rotation=0, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 10))
    ax.set_yticklabels(range(0, 101, 10), fontweight='bold')
    ax.legend(title=" ", loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)

    plt.tight_layout()
    plt.savefig('figures/Barplot.png', dpi=300, facecolor="white")
    plt.close()

    # =========================================================================
    # FIGUR 5: UTLÅNING I RELATION TILL TILLGÅNGAR (LTA) 2025
    # =========================================================================
    df_pivot["LTA"] = (df_pivot["103 Utlåning, Totalt"] / df_pivot["120 Summa tillgångar"]) * 100

    bp = df_pivot[["LTA"]].plot(kind="bar", figsize=(6, 5), color=[ratio_color], legend=False)
    bp.set_title("Utlånings-/tillgångskvot\nper december 2025", fontweight='bold', pad=10)
    bp.set_ylabel("Procent", fontweight='bold')
    bp.set_xlabel(" ")
    bp.set_xticklabels(df_pivot.index, rotation=0, fontweight='bold')
    bp.set_ylim(0, 100)
    bp.set_yticks(range(0, 101, 10))
    bp.set_yticklabels(range(0, 101, 10), fontweight='bold')

    plt.tight_layout()
    plt.savefig('figures/LTA.png', dpi=300, facecolor="white")
    plt.close()

    # =========================================================================
    # FIGUR 6: UTLÅNING I RELATION TILL INLÅNING (LTD) 2025
    # =========================================================================
    df_pivot["LTD"] = (df_pivot["103 Utlåning, Totalt"] / df_pivot["201 In-/upplåning, Totalt"]) * 100

    # Sortera för att följa din önskade ordning
    order = ["Handelsbanken", "SEB", "Swedbank"]
    df_pivot_ordered = df_pivot.loc[order]

    ax = df_pivot_ordered[["LTD"]].plot(kind="bar", color=[ratio_color], figsize=(6, 5), legend=False)
    ax.set_title("Utlånings-/inlåningskvot (System-LTD)\nper december 2025", fontweight='bold', pad=10)
    ax.set_ylabel("Procent", fontweight='bold')
    ax.set_xlabel(" ")
    ax.set_xticklabels(df_pivot_ordered.index, rotation=0, fontweight='bold')
    ax.set_ylim(0, 150)
    ax.set_yticks(range(0, 151, 10))
    ax.set_yticklabels(range(0, 151, 10), fontweight='bold')

    plt.tight_layout()
    plt.savefig('figures/LTD.png', dpi=300, facecolor="white")
    plt.close()

    print("Klart! Alla sex grafer har sparats i mappen 'figures/'.")

if __name__ == "__main__":
    main()
