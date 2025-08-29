# file: plot_best_run_dark.py
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# Sötét téma
plt.rcParams.update({
    "figure.facecolor": "#111111",
    "axes.facecolor":   "#111111",
    "axes.edgecolor":   "#DDDDDD",
    "axes.labelcolor":  "#DDDDDD",
    "text.color":       "#DDDDDD",
    "xtick.color":      "#CCCCCC",
    "ytick.color":      "#CCCCCC",
    "grid.color":       "#444444",
})

# Adat
daily = pd.read_csv("scores_daily_with_trends.csv", parse_dates=["date"]).dropna(subset=["score"])
if daily.empty:
    raise SystemExit("Nincs adat a riporthoz.")

s = pd.to_numeric(daily["score"], errors="coerce")
if not s.notna().any():
    raise SystemExit("Nincs érvényes 'score' érték.")
best = daily.loc[s.idxmax()]

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
for player, g in daily.groupby("player"):
    g = g.sort_values("date")
    ax.plot(g["date"], g["score"], marker="o", linewidth=1.5, label=player)

ax.set_title("Napi pontok – sötét mód")
ax.set_xlabel("Dátum")
ax.set_ylabel("Pont")
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.grid(True, alpha=0.4)

# Kiemelés
ax.scatter([best["date"]], [best["score"]], s=120, color="#FFD700", zorder=5)
ax.annotate(
    f"Legjobb: {best['player']} ({int(best['score'])}p)",
    xy=(best["date"], best["score"]),
    xytext=(10, -10), textcoords="offset points",
    arrowprops=dict(arrowstyle="->", color="#DDDDDD")
)

# Dátumformázás és jelmagyarázat
locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
leg = ax.legend()
leg.get_frame().set_alpha(0.2)

plt.tight_layout()

# Mentés (zárolt PDF fallback)
os.makedirs("reports", exist_ok=True)
png = os.path.join("reports", "report_best_dark.png")
pdf = os.path.join("reports", "report_best_dark.pdf")

plt.savefig(png, dpi=200, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
try:
    plt.savefig(pdf, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
    print(f"Mentve: {png}, {pdf}")
except PermissionError:
    alt = os.path.join("reports", f"report_best_dark_{int(time.time())}.pdf")
    plt.savefig(alt, bbox_inches="tight", facecolor=plt.gcf().get_facecolor())
    print(f"Mentve: {png}, {alt} (az eredeti PDF zárolt)")

plt.show()
