# analyze_scores_pandas.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

CSV = "scores.csv"
if not os.path.exists(CSV) or os.path.getsize(CSV) == 0:
    print("Hiba: A scores.csv fájl nem létezik vagy üres. Kérlek, játssz egy menetet a snake.py-val!")
    raise SystemExit(1)

# Beolvasás – toleráns hibás sorokra
df = pd.read_csv(
    CSV,
    usecols=["timestamp", "player", "score", "length", "lives_left", "tournament"],
    parse_dates=["timestamp"],
    encoding="utf-8",
    engine="python",
    on_bad_lines="skip",
)

# Napra normalizált dátum (datetime64 marad)
df["date"] = df["timestamp"].dt.normalize()

# Napi összegzés
daily = (
    df.groupby(["player", "date"], as_index=False)["score"]
      .sum()
      .sort_values(["player", "date"])
)

# Kumulált pont és 3-as gördülő átlag
daily["cum_score"] = daily.groupby("player")["score"].cumsum()
daily["roll3"] = (
    daily.groupby("player", group_keys=False)["score"]
         .rolling(window=3, min_periods=1).mean()
         .reset_index(level=0, drop=True)
)

# Mentés CSV-be
daily.to_csv("scores_daily_with_trends.csv", index=False, encoding="utf-8")
print("Mentve: scores_daily_with_trends.csv")

# Gyors kumulált grafikon
wide_cum = daily.pivot(index="date", columns="player", values="cum_score").sort_index()
ax = wide_cum.plot(title="Kumulált pontszám – gyors nézet", figsize=(9, 4))
ax.set_xlabel("Dátum")
ax.set_ylabel("Kumulált pontszám")
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

# Dinamikus időablak: utolsó 14 nap, ha van adat
if not wide_cum.empty:
    end = wide_cum.index.max()
    start = end - pd.Timedelta(days=13)
    ax.set_xlim(start, end)

ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
