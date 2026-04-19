# A/B Test Analysis — Movie Recommendation Quiz
import sys, io, urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats

SHEET_ID  = "1S3fb8LYmEot777iHeVPT1yrDSaT-jOR_63MrTzH5iDM"
TAB_NAME  = "logs"
ALPHA     = 0.05
CA, CB    = "#3498db", "#6366f1"
PLOTS_DIR = Path(__file__).parent / "plots"

def load(sheet_id, tab):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab}"
    print("Fetching data from Google Sheets...")
    with urllib.request.urlopen(url, timeout=15) as r:
        df = pd.read_csv(io.StringIO(r.read().decode()))
    print(f"  Loaded {len(df)} rows.\n")
    return df

df = load(SHEET_ID, TAB_NAME)

# Keep only the 9 expected columns, drop any unnamed extras
expected = ["session_id","group","timestamp","time_on_page","steps_completed",
            "reached_step5","genre_selections","mood_selection","made_final_pick"]
df = df[[c for c in expected if c in df.columns]].copy()

df["group"] = df["group"].str.strip().str.upper()
df = df[df["group"].isin(["A","B"])].copy()

# Fix European comma decimals e.g. "11,5" -> 11.5
df["time_on_page"] = df["time_on_page"].astype(str).str.replace(",",".").pipe(pd.to_numeric, errors="coerce")

for col in ["steps_completed","genre_selections"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in ["reached_step5","made_final_pick"]:
    df[col] = df[col].astype(str).str.strip().str.upper().map(
        {"TRUE":1,"FALSE":0,"1":1,"0":0,"1.0":1,"0.0":0})

df = df.dropna(subset=["time_on_page","steps_completed","reached_step5",
                        "genre_selections","made_final_pick"]).reset_index(drop=True)
df = df[df["time_on_page"] >= 3]

print(f"Rows after cleaning: {len(df)}  (A={len(df[df['group']=='A'])}, B={len(df[df['group']=='B'])})")

a, b = df[df["group"]=="A"], df[df["group"]=="B"]
if len(a) < 5 or len(b) < 5:
    print("Not enough data yet."); sys.exit(1)

PLOTS_DIR.mkdir(parents=True, exist_ok=True)
print("=" * 55)
print("  A/B TEST — MOVIE QUIZ ANALYSIS")
print("=" * 55)
print(f"\nGroup A: {len(a)}  |  Group B: {len(b)}\n")

desc = df.groupby("group").agg(
    n=("session_id","count"),
    mean_steps=("steps_completed","mean"),
    pct_finished=("reached_step5","mean"),
    pct_picked=("made_final_pick","mean"),
    mean_time=("time_on_page","mean"),
    mean_genres=("genre_selections","mean"),
).round(3)
desc["pct_finished"] = (desc["pct_finished"]*100).round(1).astype(str)+"%"
desc["pct_picked"]   = (desc["pct_picked"]*100).round(1).astype(str)+"%"
print("--- DESCRIPTIVE STATISTICS ---")
print(desc.to_string(), "\n")

def sig(p): return "SIGNIFICANT ✓" if p < ALPHA else "Not significant ✗"

# Test 1: Steps completed
u1, p1 = stats.mannwhitneyu(a["steps_completed"], b["steps_completed"], alternative="two-sided")
print(f"--- TEST 1: Steps Completed (Mann-Whitney U) ---")
print(f"  U={u1:.1f}, p={p1:.4f} → {sig(p1)}")
print(f"  Mean — A:{a['steps_completed'].mean():.2f}  B:{b['steps_completed'].mean():.2f}\n")

# Test 2: Reached step 5
r5a = a["reached_step5"].mean()*100; r5b = b["reached_step5"].mean()*100
print(f"--- TEST 2: Quiz Completion Rate ---")
ct2 = pd.crosstab(df["group"], df["reached_step5"])
if ct2.shape == (2,2):
    _, p2 = stats.fisher_exact(ct2)
    print(f"  Fisher's p={p2:.4f} → {sig(p2)}")
else:
    p2 = 1.0
    print(f"  No variation — both groups completed at 100%. (A positive result!)")
print(f"  A:{r5a:.1f}%  B:{r5b:.1f}%\n")

# Test 3: Made final pick
fp_a = a["made_final_pick"].mean()*100; fp_b = b["made_final_pick"].mean()*100
print(f"--- TEST 3: Made Final Movie Pick ---")
ct3 = pd.crosstab(df["group"], df["made_final_pick"])
if ct3.shape == (2,2):
    _, p3 = stats.fisher_exact(ct3)
    print(f"  Fisher's p={p3:.4f} → {sig(p3)}")
else:
    p3 = 1.0
    print(f"  No variation — all users made a final pick. (A positive result!)")
print(f"  A:{fp_a:.1f}%  B:{fp_b:.1f}%\n")

# Test 4: Time on page
u4, p4 = stats.mannwhitneyu(a["time_on_page"], b["time_on_page"], alternative="two-sided")
print(f"--- TEST 4: Time on Page (Wilcoxon Rank-Sum) ---")
print(f"  U={u4:.1f}, p={p4:.4f} → {sig(p4)}")
print(f"  Median — A:{a['time_on_page'].median():.1f}s  B:{b['time_on_page'].median():.1f}s\n")

# Test 5: Genre selections
u5, p5 = stats.mannwhitneyu(a["genre_selections"], b["genre_selections"], alternative="two-sided")
print(f"--- TEST 5: Genre Selections (Mann-Whitney U) ---")
print(f"  U={u5:.1f}, p={p5:.4f} → {sig(p5)}")
print(f"  Mean — A:{a['genre_selections'].mean():.2f}  B:{b['genre_selections'].mean():.2f}\n")

# Effect size
def cohens_d(x,y): return (y.mean()-x.mean())/np.sqrt((x.std()**2+y.std()**2)/2)
dv = cohens_d(a["time_on_page"], b["time_on_page"])
mag = "negligible" if abs(dv)<.2 else "small" if abs(dv)<.5 else "medium" if abs(dv)<.8 else "large"
print(f"--- EFFECT SIZE ---")
print(f"  Cohen's d (time_on_page, B vs A): {dv:.3f}  [{mag}]\n")

sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.dpi":150,"axes.titleweight":"bold"})

# Plot 1: Time on page boxplot
fig, ax = plt.subplots(figsize=(6,4))
bp = ax.boxplot([a["time_on_page"].values, b["time_on_page"].values],
                patch_artist=True, widths=.45,
                medianprops=dict(color="white",linewidth=2))
for patch, col in zip(bp["boxes"],[CA,CB]):
    patch.set_facecolor(col); patch.set_alpha(.75)
for i,(gdf,col) in enumerate([(a["time_on_page"],CA),(b["time_on_page"],CB)],1):
    jit = np.random.default_rng(0).uniform(-.12,.12,len(gdf))
    ax.scatter(np.full(len(gdf),i)+jit, gdf, alpha=0.3, color=col, s=18, zorder=3)
ax.set_xticks([1,2]); ax.set_xticklabels(["Version A\n(Plain)","Version B\n(Cinematic)"])
ax.set_ylabel("Time on Page (seconds)")
ax.set_title(f"Time on Page — Wilcoxon p={p4:.4f}")
ax.legend(handles=[mpatches.Patch(color=CA,alpha=.75,label="Version A"),
                   mpatches.Patch(color=CB,alpha=.75,label="Version B")])
plt.tight_layout(); plt.savefig(PLOTS_DIR/"time_boxplot.png"); plt.close()

# Plot 2: Genre selections violin
fig, ax = plt.subplots(figsize=(6,4))
vp = ax.violinplot([a["genre_selections"].values, b["genre_selections"].values],
                   positions=[1,2], showmedians=True, widths=0.6)
for pc, col in zip(vp["bodies"],[CA,CB]):
    pc.set_facecolor(col); pc.set_alpha(0.6)
for part in ("cmedians","cbars","cmaxes","cmins"):
    vp[part].set_color("white" if part=="cmedians" else "#888")
ax.set_xticks([1,2]); ax.set_xticklabels(["Version A","Version B"])
ax.set_ylabel("Genres Selected")
ax.set_title(f"Genre Selections — Mann-Whitney p={p5:.4f}")
plt.tight_layout(); plt.savefig(PLOTS_DIR/"genre_violin.png"); plt.close()

# Plot 3: Completion rates bar
fig, ax = plt.subplots(figsize=(5,4))
bars = ax.bar(["Version A","Version B"],
              [r5a, r5b], color=[CA,CB], alpha=.85, width=.45)
for bar, v in zip(bars,[r5a,r5b]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5,
            f"{v:.1f}%", ha="center", fontweight="bold", fontsize=12)
ax.set_ylim(0,110); ax.set_ylabel("Completion Rate (%)")
ax.set_title("Quiz Completion Rate")
plt.tight_layout(); plt.savefig(PLOTS_DIR/"completion_bar.png"); plt.close()

print("Plots saved to analysis/plots/\n")

print("--- FINAL SUMMARY ---")
summary = pd.DataFrame({
    "Metric":      ["Steps completed","Quiz completion","Final pick rate",
                    "Median time (s)","Mean genres"],
    "Group A":     [f"{a['steps_completed'].mean():.2f}", f"{r5a:.1f}%", f"{fp_a:.1f}%",
                    f"{a['time_on_page'].median():.1f}", f"{a['genre_selections'].mean():.2f}"],
    "Group B":     [f"{b['steps_completed'].mean():.2f}", f"{r5b:.1f}%", f"{fp_b:.1f}%",
                    f"{b['time_on_page'].median():.1f}", f"{b['genre_selections'].mean():.2f}"],
    "p-value":     [f"{p1:.4f}", "N/A", "N/A", f"{p4:.4f}", f"{p5:.4f}"],
    "Significant?":[sig(p1)[:1], "—", "—", sig(p4)[:1], sig(p5)[:1]],
})
print(summary.to_string(index=False))
print("\nAnalysis complete.")