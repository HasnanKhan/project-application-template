
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader2 import DataLoader2
from models2 import Issue, User, Label
import config

class ExampleAnalysis2:
    """
    Implements an example analysis of GitHub
    issues and outputs the result of that analysis.
    Uses models2.py to process the GitHub API JSON format.
    """

    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user)
        self.USER:str = config.get_parameter('user')

    def run(self):
        """
        Starting point for this analysis.

        Note: this is just an example analysis. You should replace the code here
        with your own implementation and then implement two more such analyses.
        """
        issues:List[Issue] = DataLoader2().get_issues()

        ### BASIC STATISTICS
        # Calculate the total number of comments for a specific user (if specified in command line args)
        # Note: Since the new format doesn't include events in the same way,
        # we'll use the comments count from the API instead
        total_comments:int = 0
        for issue in issues:
            if self.USER is None:
                total_comments += issue.comments
            # If a specific user is requested, we would need to fetch actual comment data
            # from the timeline or comments endpoint

        output:str = f'Found {total_comments} total comments across {len(issues)} issues'
        if self.USER is not None:
            output += f' (Note: filtering by user requires fetching full comment data)'
        else:
            output += '.'
        print('\n\n'+output+'\n\n')


        ### BAR CHART
        # Display a graph of the top 50 creators of issues
        top_n:int = 50
        # Create a dataframe (with only the creator's name) to make statistics a lot easier
        # Using the creator property which returns user.login
        df = pd.DataFrame.from_records([{'creator':issue.creator} for issue in issues if issue.creator])
        # Determine the number of issues for each creator and generate a bar chart of the top N
        df_hist = df.groupby(df["creator"]).value_counts().nlargest(top_n).plot(kind="bar", figsize=(14,8), title=f"Top {top_n} issue creators")
        # Set axes labels
        df_hist.set_xlabel("Creator Names")
        df_hist.set_ylabel("# of issues created")
        # Plot the chart
        # plt.show()
        # Save the chart as a PNG file
        plt.savefig('top_issue_creators2.png', bbox_inches='tight', dpi=300)



if __name__ == '__main__':
    # Invoke run method when running this module directly
    ExampleAnalysis2().run()
