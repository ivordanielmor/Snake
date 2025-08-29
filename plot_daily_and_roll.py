# 2) Javított dupla panel: napi pontok (oszlop), alatta 3-napos gördülő átlag (vonal)

# file: plot_daily_and_roll.py
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

daily = pd.read_csv("scores_daily_with_trends.csv", parse_dates=["date"]).dropna(subset=["score","roll3"])
players = daily["player"].dropna().unique().tolist()

# Játékos kiválasztás: CLI arg vagy alapértelmezett az első
player = sys.argv[1] if len(sys.argv) > 1 else players[0]
if player not in players:
    available = ", ".join(players)
    raise SystemExit(f"Ismeretlen játékos: {player}. Elérhetők: {available}")

g = daily[daily["player"] == player].sort_values("date")
if g.empty:
    raise SystemExit(f"Nincs adat: {player}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

# Felső: napi pontok
delta = g["date"].diff().median()
if pd.isna(delta) or delta <= pd.Timedelta(0):
    delta = pd.Timedelta(days=1)
width_days = 0.8 * (delta / pd.Timedelta(days=1))

ax1.bar(g["date"], g["score"], width=width_days, align="center", label="Napi pont")
ax1.set_title(f"Napi pontok – {player}")
ax1.set_ylabel("Pont")
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
ax1.grid(True, axis="y", alpha=0.3)
ax1.legend()

# Alsó: 3 napos gördülő átlag
ax2.plot(g["date"], g["roll3"], linewidth=2, label="3 napos átlag")
ax2.set_title("Gördülő átlag (3 nap)")
ax2.set_xlabel("Dátum")
ax2.set_ylabel("Pont (átlag)")
ax2.grid(True, alpha=0.3)
ax2.legend()

# Dátumformázás
ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate()

# Mentés
safe = "".join(c for c in player if c.isalnum() or c in "-_")
out = f"report_daily_roll_{safe}.png"
plt.tight_layout()
plt.savefig(out, dpi=200, bbox_inches="tight")
print(f"Játékos: {player} • Mentve: {out}")

plt.show()
