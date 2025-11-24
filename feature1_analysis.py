
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue
import config


class Feature1Analysis:
    """
    Analyzes the most common labels in GitHub issues.
    """

    def __init__(self):
        """
        Constructor
        """
        # Optional parameter to filter by specific label (passed via --label)
        self.LABEL = config.get_parameter('label')

    def run(self):
        """
        Runs the analysis to find and display the most common issue labels.
        """
        issues: List[Issue] = DataLoader().get_issues()

        # Filter by label if specified
        if self.LABEL is not None:
            issues = [issue for issue in issues if self.LABEL in issue.labels]
            print(f'\nAnalyzing {len(issues)} issues with label "{self.LABEL}"\n')
        else:
            print(f'\nAnalyzing {len(issues)} issues\n')

        # Collect all labels from all issues
        all_labels = []
        for issue in issues:
            all_labels.extend(issue.labels)

        if not all_labels:
            print("No labels found in the issues.")
            return

        # Count label occurrences
        df = pd.DataFrame({'label': all_labels})
        label_counts = df['label'].value_counts()

        print(f"[Feature 1] Most common labels:\n")
        print(label_counts)
        print(f"\nTotal unique labels: {len(label_counts)}")

        # Plot top 50 labels
        top_n = 50
        top_labels = label_counts.head(top_n)

        if not top_labels.empty:
            plt.figure(figsize=(12, 6))
            top_labels.plot(kind='bar')
            plt.title(f'Most Common Issue Labels (Top {top_n})')
            plt.xlabel('Label')
            plt.ylabel('Count')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()


if __name__ == '__main__':
    # Invoke run method when running this module directly
    Feature1Analysis().run()
