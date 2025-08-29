# file: rebuild_aggregates.py
import os
import pandas as pd

SRC = "scores.csv"

if not os.path.exists(SRC) or os.path.getsize(SRC) == 0:
    raise SystemExit("Hiányzik vagy üres a scores.csv")

# --- Beolvasás, tisztítás ---
df = pd.read_csv(
    SRC,
    parse_dates=["timestamp"],
    encoding="utf-8",
    engine="python",
    on_bad_lines="skip",
)
df = df.dropna(subset=["timestamp", "player", "score"]).copy()
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df = df.dropna(subset=["score"])

# --- Napi aggregátum + trendek ---
df["date"] = df["timestamp"].dt.normalize()
daily = (
    df.groupby(["player", "date"], as_index=False)["score"]
      .sum()
      .sort_values(["player", "date"])
)
daily["cum_score"] = daily.groupby("player")["score"].cumsum()
daily["roll3"] = (
    daily.groupby("player", group_keys=False)["score"]
         .rolling(window=3, min_periods=1).mean()
         .reset_index(level=0, drop=True)
)
daily.to_csv("scores_daily_with_trends.csv", index=False, encoding="utf-8")

# --- Heti összeg (hétvége: vasárnap) ---
week = df["timestamp"].dt.to_period("W-SUN")
df["week_end"] = week.apply(lambda p: p.end_time.normalize())

weekly = (
    df.groupby(["player", "week_end"], as_index=False)["score"]
      .sum()
      .rename(columns={"week_end": "timestamp"})
      .sort_values(["timestamp", "player"])
)
weekly.to_csv("scores_weekly.csv", index=False, encoding="utf-8")

# --- Heti kumulált (score oszlop KUMULÁLT értékkel) ---
weekly_cum = weekly.copy()
weekly_cum["score"] = (
    pd.to_numeric(weekly_cum["score"], errors="coerce").fillna(0)
)
weekly_cum["score"] = weekly_cum.groupby("player")["score"].cumsum()
weekly_cum.to_csv("scores_weekly_cum.csv", index=False, encoding="utf-8")

print(
    f"OK: daily={len(daily)} sor, weekly={len(weekly)} sor, weekly_cum={len(weekly_cum)} sor"
)
