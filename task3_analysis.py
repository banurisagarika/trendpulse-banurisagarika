"""
TrendPulse - Task 3: Analysis

This script loads cleaned CSV data,
performs analysis using pandas and numpy,
adds new columns, and saves the result.
"""

import pandas as pd
import numpy as np


# Step 1: Load and explore data
def load_data():
    df = pd.read_csv("data/trends_clean.csv")

    print(f"Loaded data: {df.shape}")

    print("\nFirst 5 rows:")
    print(df.head())

    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"\nAverage score   : {avg_score:.0f}")
    print(f"Average comments: {avg_comments:.0f}")

    return df, avg_score


# Step 2: NumPy analysis
def numpy_analysis(df):

    scores = df["score"].values

    print("\n--- NumPy Stats ---")

    print(f"Mean score   : {np.mean(scores):.0f}")
    print(f"Median score : {np.median(scores):.0f}")
    print(f"Std deviation: {np.std(scores):.0f}")

    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")

    # category with most stories
    counts = df["category"].value_counts()
    top_category = counts.idxmax()

    print(f"\nMost stories in: {top_category} ({counts.max()} stories)")

    # most commented story
    idx = df["num_comments"].idxmax()
    story = df.loc[idx]

    print(f'\nMost commented story: "{story["title"]}" — {story["num_comments"]} comments')


# Step 3: Add new columns
def add_columns(df, avg_score):

    # engagement calculation
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # popular flag
    df["is_popular"] = df["score"] > avg_score

    print("\nAdded columns: engagement, is_popular")

    return df


# Step 4: Save file
def save_file(df):

    output_path = "data/trends_analysed.csv"
    df.to_csv(output_path, index=False)

    print(f"\nSaved to {output_path}")


def main():
    print("Starting analysis...")

    df, avg_score = load_data()

    numpy_analysis(df)

    df = add_columns(df, avg_score)

    save_file(df)


if __name__ == "__main__":
    main()