Here is the requested code, tests, and README for ticket OPS-14:

**Code Implementation:**

```python
import jira
import github
from datetime import datetime

class JiraGithubSync:
    def __init__(self, jira_server, jira_auth, github_auth):
        self.jira_server = jira_server
        self.jira_client = jira.JIRA(basic_auth=jira_auth, options={'server': jira_server})
        self.github_client = github.Github(github_auth)

    def sync_issue_to_pr(self, jira_issue_key):
        jira_issue = self.jira_client.issue(jira_issue_key)
        repo_name = f"project-{jira_issue.key}"
        repo = self.github_client.get_repo(repo_name)

        # Create a new branch and commit the Jira issue as a markdown file
        branch_name = f"feature/{jira_issue.key}-{jira_issue.summary.lower().replace(' ', '-')}"
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=repo.get_commits()[0].sha)
        issue_md = self.jira_issue_to_markdown(jira_issue)
        repo.create_file(f"{jira_issue.key}.md", "Commit from Jira", issue_md)

        # Create a new PR from the branch
        title = f"Implement {jira_issue.key}: {jira_issue.fields.summary}"
        body = f"Syncing Jira issue {jira_issue_key} to GitHub\n\n{issue_md}"
        base = repo.get_branch('main')
        head = repo.get_branch(branch_name)
        pr = repo.create_pull(title, head.commit.sha, base.ref, body)

        # Add a comment to the Jira issue with the PR link
        self.jira_client.add_comment(jira_issue, f"PR created: {pr.html_url}")

    def jira_issue_to_markdown(self, jira_issue):
        markdown = f"## {jira_issue.key}: {jira_issue.fields.summary}\n"
        markdown += f"{jira_issue.fields.description}\n\n"
        markdown += "### Expected Output:\n\n"
        for i, comment in enumerate(jira_issue.fields.comment.comments, start=1):
            markdown += f"{i}. {comment.body}\n"
        return markdown

# Example usage
jira_server = 'https://your-jira-server.com'
jira_auth = ('your-jira-username', 'your-jira-api-token')
github_auth = github.GithubAuthentication(type='token', token='your-github-api-token')
sync_tool = JiraGithubSync(jira_server, jira_auth, github_auth)
sync_tool.sync_issue_to_pr('OPS-14')
```

**Unit Tests:**

```python
import unittest
from unittest.mock import patch, MagicMock
from github import Github
from jira import JIRA
from jira.resources import Comment

class TestJiraGithubSync(unittest.TestCase):
    def setUp(self):
        self.jira_server = 'https://jira-server.com'
        self.jira_auth = ('jira-user', 'jira-api-token')
        self.github_auth = Github('github-api-token')
        self.sync_tool = JiraGithub