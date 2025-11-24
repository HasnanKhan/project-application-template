
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue, Event
import config


class Feature3Analysis:
    """
    Analyzes who closed the most GitHub issues.
    """

    def __init__(self):
        """
        Constructor
        """
        # Optional parameter to filter by specific user (passed via --user)
        self.USER = config.get_parameter('user')
        # Optional parameter to filter by specific label (passed via --label)
        self.LABEL = config.get_parameter('label')

    def get_closer(self, events: List[Event]):
        """
        Extracts who closed the issue from the events.
        Returns None if the issue was never closed or author is unknown.
        """
        for event in events:
            if event.event_type == "closed" and event.author:
                return event.author
        return None

    def run(self):
        """
        Runs the analysis to find and display who closed the most issues.
        """
        issues: List[Issue] = DataLoader().get_issues()

        # Filter by label if specified
        if self.LABEL is not None:
            issues = [issue for issue in issues if self.LABEL in issue.labels]
            print(f'\nAnalyzing {len(issues)} issues with label "{self.LABEL}"')

        # Collect who closed each issue
        closers = []
        for issue in issues:
            closer = self.get_closer(issue.events)
            if closer:
                closers.append(closer)

        # Filter by user if specified
        if self.USER is not None:
            closers = [c for c in closers if c == self.USER]
            if closers:
                print(f'\nUser "{self.USER}" closed {len(closers)} issues\n')
            else:
                print(f'\nUser "{self.USER}" did not close any issues\n')
            return

        if not closers:
            print("\nNo closed issues with valid closer information found.")
            return

        # Count issues closed by each user
        df = pd.DataFrame({'closer': closers})
        closer_counts = df['closer'].value_counts()

        print(f"\n[Feature 3] Who closed the most issues:\n")
        print(closer_counts)
        print(f"\nTotal users who closed issues: {len(closer_counts)}")

        # Plot top 50 closers
        top_n = 50
        top_closers = closer_counts.head(top_n)

        if not top_closers.empty:
            plt.figure(figsize=(12, 6))
            top_closers.plot(kind='bar')
            plt.title(f'Who Closed the Most Issues (Top {top_n})')
            plt.xlabel('User')
            plt.ylabel('Issues Closed')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()


if __name__ == '__main__':
    # Invoke run method when running this module directly
    Feature3Analysis().run()
