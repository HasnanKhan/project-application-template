import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feature2_analysis import Feature2Analysis
from model import Issue, Event


class TestFeature2Analysis(unittest.TestCase):
    """
    Unit tests for Feature2Analysis class
    """

    def setUp(self):
        """Set up test fixtures"""
        # Create base dates
        self.base_date = datetime(2024, 1, 1)

        # Create mock issues with events
        self.mock_issues = [
            self._create_mock_issue_with_close(1, self.base_date, days_to_close=5),
            self._create_mock_issue_with_close(2, self.base_date, days_to_close=10),
            self._create_mock_issue_with_close(3, self.base_date, days_to_close=3),
        ]

        # Issue without closed event
        open_issue = self._create_mock_issue_with_close(4, self.base_date, days_to_close=None)
        self.mock_issues.append(open_issue)

    def _create_mock_issue_with_close(self, number, created_date, days_to_close=None):
        """Helper to create a mock issue with optional close event"""
        issue = Issue()
        issue.number = number
        issue.title = f"Test Issue {number}"
        issue.created_date = created_date
        issue.labels = ['bug']
        issue.creator = "test_user"
        issue.events = []

        if days_to_close is not None:
            # Add closed event
            closed_event = Event(None)
            closed_event.event_type = "closed"
            closed_event.author = "closer_user"
            closed_event.event_date = created_date + timedelta(days=days_to_close)
            issue.events.append(closed_event)

        return issue

    @patch('feature2_analysis.DataLoader')
    @patch('feature2_analysis.config.get_parameter')
    def test_init(self, mock_config, mock_loader):
        """Test Feature2Analysis initialization"""
        mock_config.return_value = None
        analysis = Feature2Analysis()
        self.assertIsNone(analysis.LABEL)
        mock_config.assert_called_once_with('label')

    @patch('feature2_analysis.DataLoader')
    @patch('feature2_analysis.config.get_parameter')
    def test_get_closed_date_with_closed_event(self, mock_config, mock_loader):
        """Test get_closed_date method with a closed event"""
        mock_config.return_value = None
        analysis = Feature2Analysis()

        closed_date = datetime(2024, 1, 10)
        event = Event(None)
        event.event_type = "closed"
        event.event_date = closed_date

        result = analysis.get_closed_date([event])
        self.assertEqual(result, closed_date)

    @patch('feature2_analysis.DataLoader')
    @patch('feature2_analysis.config.get_parameter')
    def test_get_closed_date_without_closed_event(self, mock_config, mock_loader):
        """Test get_closed_date method without a closed event"""
        mock_config.return_value = None
        analysis = Feature2Analysis()

        event = Event(None)
        event.event_type = "opened"

        result = analysis.get_closed_date([event])
        self.assertIsNone(result)

    @patch('feature2_analysis.DataLoader')
    @patch('feature2_analysis.config.get_parameter')
    def test_get_closed_date_empty_events(self, mock_config, mock_loader):
        """Test get_closed_date method with empty events list"""
        mock_config.return_value = None
        analysis = Feature2Analysis()

        result = analysis.get_closed_date([])
        self.assertIsNone(result)

    @patch('feature2_analysis.plt.show')
    @patch('feature2_analysis.DataLoader')
    @patch('feature2_analysis.config.get_parameter')
    def test_run_all_issues(self, mock_config, mock_loader, mock_show):
        """Test run method with all issues"""
        mock_config.return_value = None
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_issues.return_value = self.mock_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature2Analysis()
        analysis.run()

        # Verify DataLoader was called
        mock_loader_instance.get_issues.assert_called_once()
        # Verify plot was shown
        mock_show.assert_called_once()

    @patch('feature2_analysis.plt.show')
    @patch('feature2_analysis.DataLoader')
    @patch('feature2_analysis.config.get_parameter')
    def test_run_with_label_filter(self, mock_config, mock_loader, mock_show):
        """Test run method with label filter"""
        mock_config.return_value = "bug"
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_issues.return_value = self.mock_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature2Analysis()
        analysis.run()

        mock_loader_instance.get_issues.assert_called_once()
        mock_show.assert_called_once()

    @patch('feature2_analysis.DataLoader')
    @patch('feature2_analysis.config.get_parameter')
    def test_run_no_closed_issues(self, mock_config, mock_loader):
        """Test run method with no closed issues"""
        mock_config.return_value = None
        mock_loader_instance = MagicMock()
        # Create only open issues
        open_issues = [self._create_mock_issue_with_close(1, self.base_date, days_to_close=None)]
        mock_loader_instance.get_issues.return_value = open_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature2Analysis()
        # Should handle no closed issues gracefully
        analysis.run()

        mock_loader_instance.get_issues.assert_called_once()

    @patch('feature2_analysis.DataLoader')
    @patch('feature2_analysis.config.get_parameter')
    def test_time_to_close_calculation(self, mock_config, mock_loader):
        """Test that time to close is calculated correctly"""
        mock_config.return_value = None
        analysis = Feature2Analysis()

        # Issue closed after 5 days
        issue = self.mock_issues[0]
        closed_date = analysis.get_closed_date(issue.events)

        self.assertIsNotNone(closed_date)
        time_diff = (closed_date - issue.created_date).total_seconds() / (24 * 3600)
        self.assertEqual(time_diff, 5.0)


if __name__ == '__main__':
    unittest.main()
