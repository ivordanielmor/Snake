import pandas as pd
import matplotlib.pyplot as plt
import os

# Ellenőrizd, hogy a fájl létezik-e és nem üres-e
if not os.path.exists("scores.csv") or os.path.getsize("scores.csv") == 0:
    print("Hiba: A scores.csv fájl nem létezik vagy üres. Kérlek, játssz egy menetet a snake.py-val!")
    exit()

# Beolvasás
df = pd.read_csv(
    "scores.csv",
    usecols=["timestamp", "player", "score", "length", "lives_left", "tournament"],
    parse_dates=["timestamp"],
    date_format="%Y-%m-%dT%H:%M:%S",
    encoding="utf-8"
)
print("df tartalma:")
print(df)

# Dátum konverzió
df["date"] = df["timestamp"].dt.date
print("df dátum konverzió után:")
print(df)

# Napi összegzés
daily = (
    df.groupby(["player", "date"], as_index=False)["score"]
      .sum()
      .sort_values(["player", "date"])
)
print("daily tartalma:")
print(daily)

# Kumulált pontszám
daily["cum_score"] = daily.groupby("player")["score"].cumsum()
print("daily kumulált pontszám után:")
print(daily)

# 3-as gördülő átlag
daily["roll3"] = (
    daily.sort_values(["player", "date"])
         .groupby("player")["score"]
         .rolling(window=3, min_periods=1)
         .mean()
         .reset_index(level=0, drop=True)
)

# Mentés CSV-be
daily.to_csv("scores_daily_with_trends.csv", index=False, encoding="utf-8")
print("Mentve: scores_daily_with_trends.csv")

# Grafikon
wide_cum = daily.pivot(index="date", columns="player", values="cum_score")
print("wide_cum tartalma:")
print(wide_cum)
ax = wide_cum.plot(title="Kumulált pontszám – gyors nézet", figsize=(9, 4))
ax.set_xlabel("Dátum")
ax.set_ylabel("Kumulált pontszám")
# Dátumtengely korlátozása
ax.set_xlim(pd.Timestamp("2025-08-25"), pd.Timestamp("2025-08-26"))
plt.tight_layout()
plt.show()
