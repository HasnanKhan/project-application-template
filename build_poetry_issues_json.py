#!/usr/bin/env python3
import os, sys, json, time, requests

OWNER = "python-poetry"
REPO  = "poetry"
OUT   = "poetry_issues.json"

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    sys.exit("Missing GITHUB_TOKEN. `export GITHUB_TOKEN=...` and retry.")

BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"
ISSUES_URL   = f"{BASE}/issues"
TIMELINE_TPL = f"{BASE}/issues/{{number}}/timeline"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

def backoff_sleep(resp):
    if resp.status_code != 403:
        return False
    ra = resp.headers.get("Retry-After")
    if ra:
        time.sleep(max(int(ra), 1))
        return True
    rem = resp.headers.get("X-RateLimit-Remaining")
    rst = resp.headers.get("X-RateLimit-Reset")
    if rem == "0" and rst:
        sleep_s = max(int(rst) - int(time.time()) + 3, 1)
        print(f"Rate limit reached. Sleeping {sleep_s}s…", flush=True)
        time.sleep(sleep_s)
        return True
    return False

def get_paged(url, params=None):
    """Yield JSON items across all pages for a GitHub REST collection endpoint."""
    while url:
        r = requests.get(url, headers=HEADERS, params=params, timeout=60)
        if backoff_sleep(r):
            # retry same URL/params
            continue
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list):
            for item in data:
                yield item
        else:
            yield data
        # follow pagination
        url = r.links.get("next", {}).get("url")
        params = None  # only on first request

def fetch_issue_timeline(issue_number: int):
    url = TIMELINE_TPL.format(number=issue_number)
    events = []
    for e in get_paged(url, params={"per_page": 100}):
        # Timeline objects have many shapes; normalize to your required fields.
        ev_type = e.get("event") or ("commented" if "body" in e else None)
        author  = (e.get("actor") or e.get("user") or {}).get("login")
        when    = e.get("created_at") or e.get("event_at") or e.get("updated_at")
        ev = {
            "event_type": ev_type,
            "author": author,
            "event_date": when,
        }
        # Optional extras as in your example:
        if ev_type == "labeled":
            lbl = (e.get("label") or {}).get("name")
            if lbl: ev["label"] = lbl
        if ev_type == "commented" and "body" in e:
            ev["comment"] = e["body"].replace("\r", "")
        events.append({k:v for k,v in ev.items() if v is not None})
    return events

def format_issue(issue):
    return {
        "url": issue.get("html_url"),
        "creator": (issue.get("user") or {}).get("login"),
        "labels": [lbl.get("name") for lbl in issue.get("labels", []) if isinstance(lbl, dict)],
        "state": issue.get("state"),
        "assignees": [(a or {}).get("login") for a in issue.get("assignees", [])],
        "title": issue.get("title"),
        "text": (issue.get("body") or "").replace("\r", ""),  # preserve newlines, remove CR
        "number": issue.get("number"),
        "created_date": issue.get("created_at"),
        "updated_date": issue.get("updated_at"),
        "timeline_url": TIMELINE_TPL.format(number=issue.get("number")),
        "events": fetch_issue_timeline(issue.get("number")),
    }

def main():
    params = {
        "state": "all",
        "per_page": 100,
        "sort": "created",
        "direction": "asc",
    }

    all_issues = []
    count_seen = 0
    print("Fetching issues…", flush=True)
    for it in get_paged(ISSUES_URL, params=params):
        # The issues endpoint returns PRs too—skip those.
        if "pull_request" in it:
            continue
        count_seen += 1
        print(f"- Issue #{it.get('number')} …", flush=True)
        formatted = format_issue(it)
        all_issues.append(formatted)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(all_issues, f, ensure_ascii=False, indent=2)

    print(f"\nDone. Wrote {len(all_issues)} issues to {OUT}")

if __name__ == "__main__":
    main()
