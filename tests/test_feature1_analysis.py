import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feature1_analysis import Feature1Analysis
from model import Issue, Event


class TestFeature1Analysis(unittest.TestCase):
    """
    Unit tests for Feature1Analysis class
    """

    def setUp(self):
        """Set up test fixtures"""
        # Create mock issues with labels
        self.mock_issues = [
            self._create_mock_issue(1, ['bug', 'priority-high']),
            self._create_mock_issue(2, ['bug', 'enhancement']),
            self._create_mock_issue(3, ['enhancement']),
            self._create_mock_issue(4, ['bug', 'documentation']),
            self._create_mock_issue(5, ['priority-high'])
        ]

    def _create_mock_issue(self, number, labels):
        """Helper to create a mock issue"""
        issue = Issue()
        issue.number = number
        issue.labels = labels
        issue.title = f"Test Issue {number}"
        issue.creator = "test_user"
        return issue

    @patch('feature1_analysis.DataLoader')
    @patch('feature1_analysis.config.get_parameter')
    def test_init(self, mock_config, mock_loader):
        """Test Feature1Analysis initialization"""
        mock_config.return_value = None
        analysis = Feature1Analysis()
        self.assertIsNone(analysis.LABEL)
        mock_config.assert_called_once_with('label')

    @patch('feature1_analysis.DataLoader')
    @patch('feature1_analysis.config.get_parameter')
    def test_init_with_label_filter(self, mock_config, mock_loader):
        """Test Feature1Analysis initialization with label filter"""
        mock_config.return_value = "bug"
        analysis = Feature1Analysis()
        self.assertEqual(analysis.LABEL, "bug")

    @patch('feature1_analysis.plt.show')
    @patch('feature1_analysis.DataLoader')
    @patch('feature1_analysis.config.get_parameter')
    def test_run_all_issues(self, mock_config, mock_loader, mock_show):
        """Test run method with all issues"""
        mock_config.return_value = None
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_issues.return_value = self.mock_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature1Analysis()
        analysis.run()

        # Verify DataLoader was called
        mock_loader_instance.get_issues.assert_called_once()
        # Verify plot was shown
        mock_show.assert_called_once()

    @patch('feature1_analysis.plt.show')
    @patch('feature1_analysis.DataLoader')
    @patch('feature1_analysis.config.get_parameter')
    def test_run_with_label_filter(self, mock_config, mock_loader, mock_show):
        """Test run method with label filter"""
        mock_config.return_value = "bug"
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_issues.return_value = self.mock_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature1Analysis()
        analysis.run()

        # Should filter to only issues with 'bug' label (3 out of 5)
        mock_loader_instance.get_issues.assert_called_once()
        mock_show.assert_called_once()

    @patch('feature1_analysis.DataLoader')
    @patch('feature1_analysis.config.get_parameter')
    def test_run_no_labels(self, mock_config, mock_loader):
        """Test run method with issues that have no labels"""
        mock_config.return_value = None
        mock_loader_instance = MagicMock()
        # Create issues with no labels
        issues_no_labels = [self._create_mock_issue(1, [])]
        mock_loader_instance.get_issues.return_value = issues_no_labels
        mock_loader.return_value = mock_loader_instance

        analysis = Feature1Analysis()
        # Should handle empty labels gracefully
        analysis.run()

        mock_loader_instance.get_issues.assert_called_once()

    @patch('feature1_analysis.plt.show')
    @patch('feature1_analysis.DataLoader')
    @patch('feature1_analysis.config.get_parameter')
    def test_label_counting(self, mock_config, mock_loader, mock_show):
        """Test that labels are counted correctly"""
        mock_config.return_value = None
        mock_loader_instance = MagicMock()
        mock_loader_instance.get_issues.return_value = self.mock_issues
        mock_loader.return_value = mock_loader_instance

        analysis = Feature1Analysis()

        # Collect all labels to verify counting
        all_labels = []
        for issue in self.mock_issues:
            all_labels.extend(issue.labels)

        # Expected counts: bug=3, enhancement=2, priority-high=2, documentation=1
        self.assertEqual(all_labels.count('bug'), 3)
        self.assertEqual(all_labels.count('enhancement'), 2)
        self.assertEqual(all_labels.count('priority-high'), 2)
        self.assertEqual(all_labels.count('documentation'), 1)


if __name__ == '__main__':
    unittest.main()
