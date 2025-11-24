import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feature3_analysis import Feature3Analysis
from model import Issue, Event


class TestFeature3Analysis(unittest.TestCase):
    """
    Unit tests for Feature3Analysis class
    """

    def setUp(self):
        """Set up test fixtures"""
        # Create mock issues with close events
        self.mock_issues = [
            self._create_mock_issue_with_closer(1, "user_a"),
            self._create_mock_issue_with_closer(2, "user_b"),
            self._create_mock_issue_with_closer(3, "user_a"),
            self._create_mock_issue_with_closer(4, "user_c"),
            self._create_mock_issue_with_closer(5, "user_a"),
        ]

        # Issue without closer
        open_issue = self._create_mock_issue_with_closer(6, None)
        self.mock_issues.append(open_issue)

    def _create_mock_issue_with_closer(self, number, closer_username):
        """Helper to create a mock issue with optional closer"""
        issue = Issue()
        issue.number = number
        issue.title = f"Test Issue {number}"
        issue.labels = ['bug']
        issue.creator = "test_user"
        issue.events = []

        if closer_username is not None:
            # Add closed event
            closed_event = Event(None)
            closed_event.event_type = "closed"
            closed_event.author = closer_username
            closed_event.event_date = datetime(2024, 1, 1)
            issue.events.append(closed_event)

        return issue

    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_init(self, mock_config, mock_loader):
        """Test Feature3Analysis initialization"""
        mock_config.side_effect = [None, None]  # for USER and LABEL
        analysis = Feature3Analysis()
        self.assertIsNone(analysis.USER)
        self.assertIsNone(analysis.LABEL)

    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_init_with_user_filter(self, mock_config, mock_loader):
        """Test Feature3Analysis initialization with user filter"""
        mock_config.side_effect = ["user_a", None]  # for USER and LABEL
        analysis = Feature3Analysis()
        self.assertEqual(analysis.USER, "user_a")

    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_get_closer_with_closed_event(self, mock_config, mock_loader):
        """Test get_closer method with a closed event"""
        mock_config.side_effect = [None, None]
        analysis = Feature3Analysis()

        event = Event(None)
        event.event_type = "closed"
        event.author = "test_closer"

        result = analysis.get_closer([event])
        self.assertEqual(result, "test_closer")

    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_get_closer_without_closed_event(self, mock_config, mock_loader):
        """Test get_closer method without a closed event"""
        mock_config.side_effect = [None, None]
        analysis = Feature3Analysis()

        event = Event(None)
        event.event_type = "opened"

        result = analysis.get_closer([event])
        self.assertIsNone(result)

    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_get_closer_empty_events(self, mock_config, mock_loader):
        """Test get_closer method with empty events list"""
        mock_config.side_effect = [None, None]
        analysis = Feature3Analysis()

        result = analysis.get_closer([])
        self.assertIsNone(result)

    @patch('feature3_analysis.plt.show')
    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_run_all_issues(self, mock_config, mock_loader, mock_show):
        """Test run method with all issues"""
        mock_config.side_effect = [None, None]
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_issues.return_value = self.mock_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature3Analysis()
        analysis.run()

        # Verify DataLoader was called
        mock_loader_instance.get_issues.assert_called_once()
        # Verify plot was shown
        mock_show.assert_called_once()

    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_run_with_user_filter(self, mock_config, mock_loader):
        """Test run method with user filter"""
        mock_config.side_effect = ["user_a", None]
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_issues.return_value = self.mock_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature3Analysis()
        analysis.run()

        # Should filter to only issues closed by user_a (3 out of 5 closed issues)
        mock_loader_instance.get_issues.assert_called_once()

    @patch('feature3_analysis.plt.show')
    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_run_with_label_filter(self, mock_config, mock_loader, mock_show):
        """Test run method with label filter"""
        mock_config.side_effect = [None, "bug"]
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_issues.return_value = self.mock_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature3Analysis()
        analysis.run()

        mock_loader_instance.get_issues.assert_called_once()
        mock_show.assert_called_once()

    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_run_no_closers(self, mock_config, mock_loader):
        """Test run method with no closed issues"""
        mock_config.side_effect = [None, None]
        mock_loader_instance = MagicMock()
        # Create only open issues
        open_issues = [self._create_mock_issue_with_closer(1, None)]
        mock_loader_instance.get_issues.return_value = open_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature3Analysis()
        # Should handle no closers gracefully
        analysis.run()

        mock_loader_instance.get_issues.assert_called_once()

    @patch('feature3_analysis.DataLoader')
    @patch('feature3_analysis.config.get_parameter')
    def test_closer_counting(self, mock_config, mock_loader):
        """Test that closers are counted correctly"""
        mock_config.side_effect = [None, None]
        analysis = Feature3Analysis()

        # Collect all closers
        closers = []
        for issue in self.mock_issues:
            closer = analysis.get_closer(issue.events)
            if closer:
                closers.append(closer)

        # Expected counts: user_a=3, user_b=1, user_c=1
        self.assertEqual(closers.count('user_a'), 3)
        self.assertEqual(closers.count('user_b'), 1)
        self.assertEqual(closers.count('user_c'), 1)


if __name__ == '__main__':
    unittest.main()
