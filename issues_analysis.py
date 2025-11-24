import json
import pandas as pd
import matplotlib.pyplot as plt

JSON_PATH = "poetry_issues.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, list):
    issues = data
elif isinstance(data, dict):
    issues = data.get("items", [data])
else:
    raise SystemExit("Unexpected JSON structure")

df = pd.json_normalize(issues)
print(f"Loaded {len(df)} issues from {JSON_PATH}")

df["created_date"] = pd.to_datetime(df.get("created_date"), errors="coerce", utc=True)

def get_closed_info(events):
    if not isinstance(events, list):
        return None, None
    for ev in events:
        if isinstance(ev, dict) and ev.get("event_type") == "closed":
            return ev.get("event_date"), ev.get("author")
    return None, None

if "events" in df.columns:
    closed_info = df["events"].apply(get_closed_info)
    df["closed_date_raw"] = [x[0] for x in closed_info]
    df["closed_by"] = [x[1] for x in closed_info]
else:
    df["closed_date_raw"] = None
    df["closed_by"] = None

df["closed_date"] = pd.to_datetime(df["closed_date_raw"], errors="coerce", utc=True)
df["time_to_close_days"] = (
    df["closed_date"] - df["created_date"]
).dt.total_seconds() / (24 * 3600)

made_any_plot = False

# Feature 1: most common labels
if "labels" in df.columns:
    labels_exploded = df.explode("labels")
    label_counts = labels_exploded["labels"].value_counts()
    print("\n[Feature 1] Most common labels (all):\n")
    print(label_counts)

    top_labels = label_counts.head(10)
    if not top_labels.empty:
        plt.figure()
        top_labels.plot(kind="bar")
        plt.title("Most Common Issue Labels (Top 10)")
        plt.xlabel("Label")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        made_any_plot = True
else:
    print("\n[Feature 1] No 'labels' column in data.")

# Feature 2: time to close per issue
closed_df = df.dropna(subset=["time_to_close_days"])
if not closed_df.empty:
    print("\n[Feature 2] Time to close per issue (days, all):\n")
    print(
        closed_df[["number", "title", "time_to_close_days"]]
        .set_index("number")
        .round(2)
    )

    top_closed = closed_df.sort_values(
        "time_to_close_days", ascending=False
    ).head(10)

    plt.figure()
    plt.bar(
        top_closed["number"].astype(str),
        top_closed["time_to_close_days"],
    )
    plt.title("Time to Close per Issue (Top 10 Longest, Days)")
    plt.xlabel("Issue Number")
    plt.ylabel("Days")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    made_any_plot = True
else:
    print("\n[Feature 2] No closed issues with valid dates.")

# Feature 3: who closed the most issues
if "closed_by" in df.columns and not closed_df.empty:
    closer_counts = closed_df["closed_by"].dropna().value_counts()
    print("\n[Feature 3] Who closed the most issues (all):\n")
    print(closer_counts)

    top_closers = closer_counts.head(10)
    if not top_closers.empty:
        plt.figure()
        top_closers.plot(kind="bar")
        plt.title("Who Closed the Most Issues (Top 10)")
        plt.xlabel("User")
        plt.ylabel("Issues Closed")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        made_any_plot = True
    else:
        print("[Feature 3] No 'closed_by' data found.")
else:
    print("\n[Feature 3] No 'closed_by' column or no closed issues.")

if made_any_plot:
    plt.show()
