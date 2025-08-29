# file: plot_weekly.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

CSV = "scores_weekly.csv"
if not os.path.exists(CSV) or os.path.getsize(CSV) == 0:
    raise SystemExit("Hiányzó vagy üres: scores_weekly.csv")

# Beolvasás és tisztítás
df = pd.read_csv(CSV, parse_dates=["timestamp"])
df = df.dropna(subset=["timestamp", "player", "score"]).copy()
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df = df.dropna(subset=["score"])
df["week"] = df["timestamp"].dt.normalize()

# Heti összeg játékosonként (ha duplikált sorok lennének)
df = (df.groupby(["week", "player"], as_index=False)["score"].sum()).sort_values(["week", "score"], ascending=[True, False])

weeks = df["week"].unique()
players = sorted(df["player"].unique().tolist())

if len(weeks) == 1:
    # Egy hét: rangsor vízszintes oszlopokkal
    g = df.sort_values("score", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(g["player"], g["score"])
    ax.set_title(f"Heti pontok – {pd.to_datetime(weeks[0]).date()}")
    ax.set_xlabel("Pont")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    for i, v in enumerate(g["score"]):
        ax.text(v, i, f" {int(v)}", va="center")
    plt.tight_layout()
    plt.savefig("report_weekly.png", dpi=200, bbox_inches="tight")
    plt.savefig("report_weekly.pdf", bbox_inches="tight")
    plt.show()
else:
    # Több hét: vonaldiagram játékosonként
    wide = (df.pivot(index="week", columns="player", values="score")
              .reindex(columns=players)
              .sort_index())
    fig, ax = plt.subplots(figsize=(10, 5))
    wide.plot(ax=ax, marker="o", linewidth=2)
    ax.set_title("Heti pontok játékosonként")
    ax.set_xlabel("Hét")
    ax.set_ylabel("Pont")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    loc = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("report_weekly.png", dpi=200, bbox_inches="tight")
    plt.savefig("report_weekly.pdf", bbox_inches="tight")
    plt.show()
