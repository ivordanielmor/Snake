# 1) Szépített kumulált pontgrafikon (jelmagyarázattal, dátumformázással)
# Kiinduló fájl: scores_daily_with_trends.csv (oszlopok: player, date, score, cum_score, roll3)
# file: plot_cumulative_scores.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

CSV = "scores_daily_with_trends.csv"
if not os.path.exists(CSV) or os.path.getsize(CSV) == 0:
    raise SystemExit("Hiba: scores_daily_with_trends.csv nem létezik vagy üres.")

daily = pd.read_csv(CSV, parse_dates=["date"]).dropna(subset=["cum_score"])

fig, ax = plt.subplots(figsize=(10, 5))

last_rows = []
for player, g in daily.groupby("player"):
    g = g.sort_values("date")
    ax.plot(g["date"], g["cum_score"], marker="o", linewidth=2, markersize=4, label=player)
    last_rows.append({"player": player, "x": g["date"].iloc[-1], "y": float(g["cum_score"].iloc[-1])})

# jobb oldali nem-ütköző címkék
last = pd.DataFrame(last_rows).sort_values("y").reset_index(drop=True)
if not last.empty:
    x_anchor = last["x"].max() + pd.Timedelta(days=1)
    y_vals = last["y"].to_list()
    y_range = max(1.0, max(y_vals) - min(y_vals))
    min_gap = max(1.0, 0.06 * y_range)

    spread = []
    for v in y_vals:
        spread.append(v if not spread else max(v, spread[-1] + min_gap))

    for row, ylab in zip(last.to_dict("records"), spread):
        ax.plot([row["x"], x_anchor], [row["y"], ylab], linestyle=":", linewidth=1, alpha=0.7)
        ax.text(x_anchor, ylab, f'{row["player"]}: {int(row["y"])}', ha="left", va="center")

    ax.set_xlim(daily["date"].min(), x_anchor + pd.Timedelta(days=2))
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(min(ymin, min(y_vals) - min_gap), max(ymax, max(spread) + min_gap))

ax.set_title("Kumulált pontszámok – Snake")
ax.set_xlabel("Dátum")
ax.set_ylabel("Kumulált pontszám")
ax.grid(True, alpha=0.3)
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.legend(loc="upper left")

ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate()

plt.tight_layout()
plt.savefig("report_cumulative.png", dpi=200, bbox_inches="tight")
plt.show()
