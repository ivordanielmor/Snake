# file: summary_dashboard.py
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# --- CLI ---
p = argparse.ArgumentParser(description="Összefoglaló dashboard")
p.add_argument("--player", help="Kiválasztott játékos neve", default=None)
p.add_argument("--infile", help="Bemenet (scores_daily_with_trends.csv)", default="scores_daily_with_trends.csv")
p.add_argument("--out", help="Kimeneti PNG", default="reports/summary_dashboard.png")
args = p.parse_args()

# --- Adat ---
if not os.path.exists(args.infile) or os.path.getsize(args.infile) == 0:
    raise SystemExit("Hiányzik a scores_daily_with_trends.csv")

daily = pd.read_csv(args.infile, parse_dates=["date"]).dropna(subset=["player","date","score","cum_score","roll3"])
players = daily["player"].dropna().unique().tolist()
players.sort()

sel = args.player or (players[0] if players else None)
if sel not in players:
    raise SystemExit(f"Ismeretlen játékos: {sel}. Elérhetők: {', '.join(players)}")

g_sel = daily[daily["player"] == sel].sort_values("date")
if g_sel.empty:
    raise SystemExit(f"Nincs adat: {sel}")

# --- Ábra ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 9), sharex=False)

# 1) Kumulált pontok minden játékosnak
for pl, g in daily.groupby("player"):
    g = g.sort_values("date")
    ax1.plot(g["date"], g["cum_score"], marker="o", linewidth=2, label=pl)
ax1.set_title("Kumulált pontok játékosonként")
ax1.set_ylabel("Pont")
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
ax1.grid(True, alpha=0.3)
ax1.legend(ncol=2)
loc1 = mdates.AutoDateLocator()
ax1.xaxis.set_major_locator(loc1)
ax1.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc1))

# 2) Napi pontok (oszlop) kiválasztott játékosra
delta = g_sel["date"].diff().median()
if pd.isna(delta) or delta <= pd.Timedelta(0):
    delta = pd.Timedelta(days=1)
width_days = 0.8 * (delta / pd.Timedelta(days=1))
ax2.bar(g_sel["date"], g_sel["score"], width=width_days, align="center", label=f"Napi pont – {sel}")
ax2.set_title(f"Napi pontok – {sel}")
ax2.set_ylabel("Pont")
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
ax2.grid(True, axis="y", alpha=0.3)
ax2.legend()
loc2 = mdates.AutoDateLocator()
ax2.xaxis.set_major_locator(loc2)
ax2.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc2))

# 3) 3 napos gördülő átlag (több játékos)
for pl, g in daily.groupby("player"):
    g = g.sort_values("date")
    ax3.plot(g["date"], g["roll3"], linewidth=2, label=pl)
ax3.set_title("Gördülő átlag (3 nap)")
ax3.set_xlabel("Dátum")
ax3.set_ylabel("Pont (átlag)")
ax3.grid(True, alpha=0.3)
ax3.legend(ncol=2)
loc3 = mdates.AutoDateLocator()
ax3.xaxis.set_major_locator(loc3)
ax3.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc3))

plt.tight_layout()

# --- Mentés ---
os.makedirs(os.path.dirname(args.out), exist_ok=True)
plt.savefig(args.out, dpi=200, bbox_inches="tight")
print(f"Mentve: {args.out}")
plt.show()
