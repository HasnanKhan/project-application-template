"""
Implements a runtime data model that can be used to access
the properties contained in the issues JSON (GitHub API format).
This model handles the raw GitHub API response format.
"""

from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
from dateutil import parser


class State(str, Enum):
    """
    Whether issue is open or closed.
    """
    open = 'open'
    closed = 'closed'


class User:
    """
    Represents a GitHub user object.
    """

    def __init__(self, jobj: Optional[Dict[str, Any]] = None):
        self.login: Optional[str] = None
        self.id: Optional[int] = None
        self.node_id: Optional[str] = None
        self.avatar_url: Optional[str] = None
        self.gravatar_id: Optional[str] = None
        self.url: Optional[str] = None
        self.html_url: Optional[str] = None
        self.followers_url: Optional[str] = None
        self.following_url: Optional[str] = None
        self.gists_url: Optional[str] = None
        self.starred_url: Optional[str] = None
        self.subscriptions_url: Optional[str] = None
        self.organizations_url: Optional[str] = None
        self.repos_url: Optional[str] = None
        self.events_url: Optional[str] = None
        self.received_events_url: Optional[str] = None
        self.type: Optional[str] = None
        self.user_view_type: Optional[str] = None
        self.site_admin: bool = False

        if jobj is not None:
            self.from_json(jobj)

    def from_json(self, jobj: Dict[str, Any]):
        self.login = jobj.get('login')
        self.id = jobj.get('id')
        self.node_id = jobj.get('node_id')
        self.avatar_url = jobj.get('avatar_url')
        self.gravatar_id = jobj.get('gravatar_id')
        self.url = jobj.get('url')
        self.html_url = jobj.get('html_url')
        self.followers_url = jobj.get('followers_url')
        self.following_url = jobj.get('following_url')
        self.gists_url = jobj.get('gists_url')
        self.starred_url = jobj.get('starred_url')
        self.subscriptions_url = jobj.get('subscriptions_url')
        self.organizations_url = jobj.get('organizations_url')
        self.repos_url = jobj.get('repos_url')
        self.events_url = jobj.get('events_url')
        self.received_events_url = jobj.get('received_events_url')
        self.type = jobj.get('type')
        self.user_view_type = jobj.get('user_view_type')
        self.site_admin = jobj.get('site_admin', False)


class Label:
    """
    Represents a GitHub label object.
    """

    def __init__(self, jobj: Optional[Dict[str, Any]] = None):
        self.id: Optional[int] = None
        self.node_id: Optional[str] = None
        self.url: Optional[str] = None
        self.name: Optional[str] = None
        self.color: Optional[str] = None
        self.default: bool = False
        self.description: Optional[str] = None

        if jobj is not None:
            self.from_json(jobj)

    def from_json(self, jobj: Dict[str, Any]):
        self.id = jobj.get('id')
        self.node_id = jobj.get('node_id')
        self.url = jobj.get('url')
        self.name = jobj.get('name')
        self.color = jobj.get('color')
        self.default = jobj.get('default', False)
        self.description = jobj.get('description')


class Reactions:
    """
    Represents GitHub reactions to an issue.
    """

    def __init__(self, jobj: Optional[Dict[str, Any]] = None):
        self.url: Optional[str] = None
        self.total_count: int = 0
        self.plus_one: int = 0
        self.minus_one: int = 0
        self.laugh: int = 0
        self.hooray: int = 0
        self.confused: int = 0
        self.heart: int = 0
        self.rocket: int = 0
        self.eyes: int = 0

        if jobj is not None:
            self.from_json(jobj)

    def from_json(self, jobj: Dict[str, Any]):
        self.url = jobj.get('url')
        self.total_count = jobj.get('total_count', 0)
        self.plus_one = jobj.get('+1', 0)
        self.minus_one = jobj.get('-1', 0)
        self.laugh = jobj.get('laugh', 0)
        self.hooray = jobj.get('hooray', 0)
        self.confused = jobj.get('confused', 0)
        self.heart = jobj.get('heart', 0)
        self.rocket = jobj.get('rocket', 0)
        self.eyes = jobj.get('eyes', 0)


class Issue:
    """
    Represents a GitHub issue (raw API format).
    """

    def __init__(self, jobj: Optional[Dict[str, Any]] = None):
        self.url: Optional[str] = None
        self.repository_url: Optional[str] = None
        self.labels_url: Optional[str] = None
        self.comments_url: Optional[str] = None
        self.events_url: Optional[str] = None
        self.html_url: Optional[str] = None
        self.id: Optional[int] = None
        self.node_id: Optional[str] = None
        self.number: int = -1
        self.title: Optional[str] = None
        self.user: Optional[User] = None
        self.labels: List[Label] = []
        self.state: Optional[State] = None
        self.locked: bool = False
        self.assignee: Optional[User] = None
        self.assignees: List[User] = []
        self.milestone: Optional[Dict[str, Any]] = None
        self.comments: int = 0
        self.created_at: Optional[datetime] = None
        self.updated_at: Optional[datetime] = None
        self.closed_at: Optional[datetime] = None
        self.author_association: Optional[str] = None
        self.active_lock_reason: Optional[str] = None
        self.body: Optional[str] = None
        self.closed_by: Optional[User] = None
        self.reactions: Optional[Reactions] = None
        self.timeline_url: Optional[str] = None
        self.performed_via_github_app: Optional[Dict[str, Any]] = None
        self.state_reason: Optional[str] = None
        self.sub_issues_summary: Optional[Dict[str, Any]] = None
        self.issue_dependencies_summary: Optional[Dict[str, Any]] = None

        # Additional fields that may be present
        self.type: Optional[str] = None

        if jobj is not None:
            self.from_json(jobj)

    def from_json(self, jobj: Dict[str, Any]):
        self.url = jobj.get('url')
        self.repository_url = jobj.get('repository_url')
        self.labels_url = jobj.get('labels_url')
        self.comments_url = jobj.get('comments_url')
        self.events_url = jobj.get('events_url')
        self.html_url = jobj.get('html_url')
        self.id = jobj.get('id')
        self.node_id = jobj.get('node_id')

        try:
            self.number = int(jobj.get('number', '-1'))
        except (ValueError, TypeError):
            self.number = -1

        self.title = jobj.get('title')

        # Parse user object
        user_data = jobj.get('user')
        if user_data:
            self.user = User(user_data)

        # Parse labels
        labels_data = jobj.get('labels', [])
        self.labels = [Label(label) for label in labels_data]

        # Parse state
        state_str = jobj.get('state')
        if state_str:
            try:
                self.state = State[state_str]
            except KeyError:
                self.state = None

        self.locked = jobj.get('locked', False)

        # Parse assignee
        assignee_data = jobj.get('assignee')
        if assignee_data:
            self.assignee = User(assignee_data)

        # Parse assignees
        assignees_data = jobj.get('assignees', [])
        self.assignees = [User(assignee) for assignee in assignees_data]

        self.milestone = jobj.get('milestone')
        self.comments = jobj.get('comments', 0)

        # Parse dates
        try:
            created_at_str = jobj.get('created_at')
            if created_at_str:
                self.created_at = parser.parse(created_at_str)
        except (ValueError, TypeError):
            pass

        try:
            updated_at_str = jobj.get('updated_at')
            if updated_at_str:
                self.updated_at = parser.parse(updated_at_str)
        except (ValueError, TypeError):
            pass

        try:
            closed_at_str = jobj.get('closed_at')
            if closed_at_str:
                self.closed_at = parser.parse(closed_at_str)
        except (ValueError, TypeError):
            pass

        self.author_association = jobj.get('author_association')
        self.active_lock_reason = jobj.get('active_lock_reason')
        self.body = jobj.get('body')

        # Parse closed_by
        closed_by_data = jobj.get('closed_by')
        if closed_by_data:
            self.closed_by = User(closed_by_data)

        # Parse reactions
        reactions_data = jobj.get('reactions')
        if reactions_data:
            self.reactions = Reactions(reactions_data)

        self.timeline_url = jobj.get('timeline_url')
        self.performed_via_github_app = jobj.get('performed_via_github_app')
        self.state_reason = jobj.get('state_reason')
        self.sub_issues_summary = jobj.get('sub_issues_summary')
        self.issue_dependencies_summary = jobj.get('issue_dependencies_summary')
        self.type = jobj.get('type')

    # Convenience properties for compatibility with the old model
    @property
    def creator(self) -> Optional[str]:
        """Returns the username of the issue creator."""
        return self.user.login if self.user else None

    @property
    def text(self) -> Optional[str]:
        """Returns the issue body text."""
        return self.body

    @property
    def created_date(self) -> Optional[datetime]:
        """Returns the creation date."""
        return self.created_at

    @property
    def updated_date(self) -> Optional[datetime]:
        """Returns the updated date."""
        return self.updated_at

    @property
    def label_names(self) -> List[str]:
        """Returns a list of label names."""
        return [label.name for label in self.labels if label.name]
