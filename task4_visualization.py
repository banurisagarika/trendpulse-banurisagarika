"""
TrendPulse - Task 4: Visualisation
====================================
Loads the analysed CSV from Task 3 and produces 3 individual
charts plus a combined dashboard, all saved as PNG files.

Pipeline position: Task 1 → Task 2 → Task 3 → Task 4 ✓
Input : data/trends_analysed.csv   (from Task 3)
Output: outputs/chart1_top_stories.png
        outputs/chart2_categories.png
        outputs/chart3_scatter.png
       
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



# STEP 1: Setup — load data and create outputs/

def setup():
   

    # Create the output folder for PNG files
    os.makedirs("outputs", exist_ok=True)

    # Load the CSV produced by Task 3
    df = pd.read_csv("data/trends_analysed.csv")

    # is_popular was saved as True/False strings in CSV — cast to bool
    df["is_popular"] = df["is_popular"].astype(bool)

    print(f"Loaded {len(df)} rows from data/trends_analysed.csv")
    return df


def shorten(title, max_len=50):
    """
    If a title is longer than max_len characters, truncate it
    and add '…' so bar labels stay readable on the chart.
    """
    return title if len(title) <= max_len else title[:max_len] + "…"



# CHART 1: Top 10 Stories by Score (horizontal bar)


def chart1_top_stories(df):
    # Sort by score descending and take the top 10
    top10 = df.nlargest(10, "score").copy()

    # Shorten any title that is over 50 characters
    top10["short_title"] = top10["title"].apply(shorten)

    fig, ax = plt.subplots(figsize=(12, 6))

    # barh draws horizontal bars; y = title, width = score
    bars = ax.barh(
        top10["short_title"],
        top10["score"],
        color="#4C72B0",   # consistent blue across chart 1
        edgecolor="white",
        height=0.6,
    )

    # Reverse order so the highest score appears at the top
    ax.invert_yaxis()

    # Add score value labels at the end of each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.5,               # slight offset to the right
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,}",         # formatted integer
            va="center", fontsize=8,
        )

    ax.set_title("Top 10 HackerNews Stories by Score", fontsize=14, pad=12)
    ax.set_xlabel("Score (upvotes)")
    ax.set_ylabel("Story Title")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    # Always savefig BEFORE show so the file is written correctly
    plt.savefig("outputs/chart1_top_stories.png", dpi=150)
    plt.close()   # free memory; we do not call plt.show() here

    print("Saved: outputs/chart1_top_stories.png")



# CHART 2: Stories per Category (vertical bar)


def chart2_categories(df):

    # Count stories in each category; sort by count descending
    category_counts = df["category"].value_counts().sort_values(ascending=False)

    # One distinct colour per category bar
    colours = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(
        category_counts.index,
        category_counts.values,
        color=colours[: len(category_counts)],
        edgecolor="white",
        width=0.55,
    )

    # Label each bar with its count above the bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.3,
            str(int(height)),
            ha="center", va="bottom", fontsize=10,
        )

    ax.set_title("Number of Stories per Category", fontsize=14, pad=12)
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Stories")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("outputs/chart2_categories.png", dpi=150)
    plt.close()

    print("Saved: outputs/chart2_categories.png")



# CHART 3: Score vs Comments (scatter plot)


def chart3_scatter(df):
    

    # Split the DataFrame into two groups for separate colouring
    popular     = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    fig, ax = plt.subplots(figsize=(9, 6))

    # Plot non-popular stories first (they sit behind popular ones)
    ax.scatter(
        not_popular["score"],
        not_popular["num_comments"],
        color="#AEC6E8",   # light blue for below-average stories
        alpha=0.7,
        s=50,
        label="Not Popular",
        edgecolors="white",
        linewidths=0.4,
    )

    # Plot popular stories on top with a contrasting colour
    ax.scatter(
        popular["score"],
        popular["num_comments"],
        color="#C44E52",   # red for above-average stories
        alpha=0.85,
        s=70,
        label="Popular (above avg score)",
        edgecolors="white",
        linewidths=0.4,
    )

    ax.set_title("Score vs Number of Comments", fontsize=14, pad=12)
    ax.set_xlabel("Score (upvotes)")
    ax.set_ylabel("Number of Comments")
    ax.legend(framealpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("outputs/chart3_scatter.png", dpi=150)
    plt.close()

    print("Saved: outputs/chart3_scatter.png")


# ─────────────────────────────────────────────
# BONUS: Combined Dashboard (1 × 3 layout)
# ─────────────────────────────────────────────

def chart_dashboard(df):
  

    fig, axes = plt.subplots(1, 3, figsize=(22, 7))
    fig.suptitle("TrendPulse Dashboard", fontsize=18, fontweight="bold", y=1.01)

    # ── Panel 1: Top 10 stories ──────────────────────
    top10 = df.nlargest(10, "score").copy()
    top10["short_title"] = top10["title"].apply(shorten)

    axes[0].barh(
        top10["short_title"], top10["score"],
        color="#4C72B0", edgecolor="white", height=0.6,
    )
    axes[0].invert_yaxis()
    axes[0].set_title("Top 10 Stories by Score", fontsize=11)
    axes[0].set_xlabel("Score")
    axes[0].tick_params(axis="y", labelsize=7)
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    # ── Panel 2: Stories per category ────────────────
    colours = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]
    cat_counts = df["category"].value_counts().sort_values(ascending=False)

    axes[1].bar(
        cat_counts.index, cat_counts.values,
        color=colours[: len(cat_counts)], edgecolor="white", width=0.55,
    )
    axes[1].set_title("Stories per Category", fontsize=11)
    axes[1].set_xlabel("Category")
    axes[1].set_ylabel("Count")
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)

    # ── Panel 3: Score vs Comments scatter ───────────
    popular     = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    axes[2].scatter(
        not_popular["score"], not_popular["num_comments"],
        color="#AEC6E8", alpha=0.7, s=40,
        label="Not Popular", edgecolors="white", linewidths=0.3,
    )
    axes[2].scatter(
        popular["score"], popular["num_comments"],
        color="#C44E52", alpha=0.85, s=55,
        label="Popular", edgecolors="white", linewidths=0.3,
    )
    axes[2].set_title("Score vs Comments", fontsize=11)
    axes[2].set_xlabel("Score")
    axes[2].set_ylabel("Comments")
    axes[2].legend(fontsize=8, framealpha=0.9)
    axes[2].spines["top"].set_visible(False)
    axes[2].spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("Saved: outputs/dashboard.png")


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  TrendPulse — Task 4: Visualisation")
    print("=" * 50)

    # 1. Load data and create outputs/ folder
    df = setup()

    # 2. Chart 1 — horizontal bar: top 10 stories by score
    chart1_top_stories(df)

    # 3. Chart 2 — bar: number of stories per category
    chart2_categories(df)

    # 4. Chart 3 — scatter: score vs comments coloured by popularity
    chart3_scatter(df)

    # Bonus — combined dashboard with all 3 panels
    chart_dashboard(df)

    print("\nAll charts saved to outputs/")
    print("Pipeline complete: collect → clean → analyse → visualise ✓")


if __name__ == "__main__":
    main()