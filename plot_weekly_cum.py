# file: plot_weekly_cum.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

CSV = "scores_weekly_cum.csv"
if not os.path.exists(CSV) or os.path.getsize(CSV) == 0:
    raise SystemExit("Hiányzó vagy üres: scores_weekly_cum.csv")

df = pd.read_csv(CSV, parse_dates=["timestamp"])
df = df.dropna(subset=["timestamp", "player", "score"])
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df = df.dropna(subset=["score"])

weeks = df["timestamp"].dt.normalize().unique()

if len(weeks) == 1:
    # Egy hét: rangsor vízszintes oszlopokkal
    g = (df.groupby("player", as_index=False)["score"]
           .sum()
           .sort_values("score", ascending=False))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(g["player"], g["score"])
    ax.set_title(f"Heti kumulált pontszámok – {pd.to_datetime(weeks[0]).date()}")
    ax.set_xlabel("Pont")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    for i, v in enumerate(g["score"]):
        ax.text(v, i, f" {int(v)}", va="center")
    plt.tight_layout()
    plt.savefig("report_weekly_cum.png", dpi=200, bbox_inches="tight")
    plt.savefig("report_weekly_cum.pdf", bbox_inches="tight")
    plt.show()
else:
    # Több hét: vonaldiagram játékosonként
    wide = (df.pivot_table(index="timestamp", columns="player", values="score", aggfunc="sum")
              .sort_index())
    fig, ax = plt.subplots(figsize=(10, 5))
    wide.plot(ax=ax, marker="o")
    ax.set_title("Heti kumulált pontszámok játékosonként")
    ax.set_xlabel("Hét")
    ax.set_ylabel("Pont")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    loc = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("report_weekly_cum.png", dpi=200, bbox_inches="tight")
    plt.savefig("report_weekly_cum.pdf", bbox_inches="tight")
    plt.show()
