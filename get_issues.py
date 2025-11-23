"""
Script to fetch GitHub issues from the python-poetry/poetry repository
and save them to a JSON file.
"""

import requests
import json
from typing import List, Dict, Any


def fetch_issues(repo_url: str = "https://api.github.com/repos/python-poetry/poetry/issues") -> List[Dict[str, Any]]:
    """
    Fetch all issues from the GitHub API using cursor-based pagination.

    Args:
        repo_url: The GitHub API URL for the repository issues

    Returns:
        A list of issue dictionaries
    """
    all_issues = []
    per_page = 100  # Maximum allowed by GitHub API
    page_count = 0

    # Start with initial URL
    url = repo_url
    params = {
        'per_page': per_page,
        'state': 'all'  # Get both open and closed issues
    }

    while url:
        page_count += 1
        print(f"Fetching page {page_count}...")

        response = requests.get(url, params=params)

        # Check if request was successful
        if response.status_code != 200:
            print(f"Error fetching issues: {response.status_code}")
            print(f"Response: {response.text}")
            break

        issues = response.json()

        # If no more issues, we're done
        if not issues:
            break

        all_issues.extend(issues)
        print(f"  Retrieved {len(issues)} issues (total so far: {len(all_issues)})")

        # Parse the Link header to get the next page URL
        # GitHub uses cursor-based pagination via the Link header
        link_header = response.headers.get('Link', '')
        url = None  # Reset URL
        params = {}  # Clear params for next iteration (they're in the URL)

        if link_header:
            # Parse Link header to find 'next' relation
            links = link_header.split(',')
            for link in links:
                if 'rel="next"' in link:
                    # Extract URL from <URL>; rel="next"
                    url = link[link.find('<')+1:link.find('>')]
                    break

    return all_issues


def save_issues_to_json(issues: List[Dict[str, Any]], filename: str = "poetry_issues2.json") -> None:
    """
    Save issues to a JSON file.

    Args:
        issues: List of issue dictionaries
        filename: Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(issues)} issues to {filename}")


def main():
    """
    Main function to fetch issues and save to JSON file.
    """
    print("Fetching issues from python-poetry/poetry repository...\n")

    issues = fetch_issues()

    if issues:
        save_issues_to_json(issues)
    else:
        print("No issues fetched.")


if __name__ == '__main__':
    main()
