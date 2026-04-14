"""
TrendPulse - Task 2: Data Processing
"""

import os
import glob
import pandas as pd


# Step 1: Load JSON file
def load_json():
    # find all json files created from task 1
    files = glob.glob("data/trends_*.json")

    # remove any cleaned files if present
    json_files = [f for f in files if "clean" not in f]

    if not json_files:
        print("No JSON file found. Please run Task 1 first.")
        exit()

    # pick latest file
    latest_file = max(json_files, key=os.path.getmtime)

    df = pd.read_json(latest_file)

    print(f"Loaded {len(df)} stories from {latest_file}")
    return df


# Step 2: Clean data
def clean_data(df):

    # remove duplicates
    df = df.drop_duplicates(subset=["post_id"])
    print(f"\nAfter removing duplicates: {len(df)}")

    # remove missing important fields
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # fix data types
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)
    df["post_id"] = df["post_id"].astype(int)

    # remove low score stories
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # remove extra spaces in title
    df["title"] = df["title"].str.strip()

    return df


# Step 3: Save to CSV
def save_csv(df):

    os.makedirs("data", exist_ok=True)

    file_path = "data/trends_clean.csv"

    df.to_csv(file_path, index=False)

    print(f"\nSaved {len(df)} rows to {file_path}")

    # category summary
    print("\nStories per category:")
    counts = df["category"].value_counts()

    for cat, count in counts.items():
        print(f"  {cat:<15} {count}")


# main function
def main():

    print("Starting data cleaning...")

    df = load_json()

    df_clean = clean_data(df)

    save_csv(df_clean)


if __name__ == "__main__":
    main()