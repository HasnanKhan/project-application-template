
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue, Event
import config


class Feature2Analysis:
    """
    Analyzes time to close for GitHub issues.
    """

    def __init__(self):
        """
        Constructor
        """
        # Optional parameter to filter by specific label (passed via --label)
        self.LABEL = config.get_parameter('label')

    def get_closed_date(self, events: List[Event]):
        """
        Extracts the closed date from issue events.
        Returns None if the issue was never closed.
        """
        for event in events:
            if event.event_type == "closed" and event.event_date:
                return event.event_date
        return None

    def run(self):
        """
        Runs the analysis to calculate and display time to close for issues.
        """
        issues: List[Issue] = DataLoader().get_issues()

        # Filter by label if specified
        if self.LABEL is not None:
            issues = [issue for issue in issues if self.LABEL in issue.labels]
            print(f'\nAnalyzing {len(issues)} issues with label "{self.LABEL}"\n')
        else:
            print(f'\nAnalyzing {len(issues)} issues\n')

        # Calculate time to close for each issue
        issue_data = []
        for issue in issues:
            closed_date = self.get_closed_date(issue.events)
            if closed_date and issue.created_date:
                time_to_close_days = (closed_date - issue.created_date).total_seconds() / (24 * 3600)
                issue_data.append({
                    'number': issue.number,
                    'title': issue.title,
                    'time_to_close_days': time_to_close_days
                })

        if not issue_data:
            print("No closed issues with valid dates found.")
            return

        # Create DataFrame for analysis
        df = pd.DataFrame(issue_data)

        print(f"[Feature 2] Time to close per issue (days):\n")
        print(df[['number', 'title', 'time_to_close_days']].set_index('number').round(2))
        print(f"\nAverage time to close: {df['time_to_close_days'].mean():.2f} days")
        print(f"Median time to close: {df['time_to_close_days'].median():.2f} days")

        # Plot top 50 longest time to close
        top_n = 50
        top_issues = df.nlargest(top_n, 'time_to_close_days')

        plt.figure(figsize=(12, 6))
        plt.bar(
            top_issues['number'].astype(str),
            top_issues['time_to_close_days']
        )
        plt.title(f'Time to Close per Issue (Top {top_n} Longest, Days)')
        plt.xlabel('Issue Number')
        plt.ylabel('Days')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    # Invoke run method when running this module directly
    Feature2Analysis().run()
