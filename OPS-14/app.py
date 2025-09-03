Sure! Here is the code, tests, and instructions based on the provided Jira ticket:

## Code Implementation:

```python
import jira
import github
from datetime import datetime

class JiraGithubSync:
    def __init__(self, jira_server, jira_auth, github_auth):
        self.jira_server = jira_server
        self.jira_client = jira.JIRA(basic_auth=jira_auth)
        self.github_client = github.Github(github_auth)

    def sync_issue_to_pr(self, jira_issue_id):
        jira_issue = self.jira_client.issue(jira_issue_id)
        repo_name = f"project-{jira_issue.key}"
        repo = self.github_client.get_repo(repo_name)

        # Create a new branch and commit the Jira issue as a Markdown file
        branch_name = f"jira-issue-{jira_issue.key}"
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=repo.get_commits()[0].sha)
        issue_md = self.jira_issue_to_markdown(jira_issue)
        repo.create_file(f"{jira_issue.key}.md", branch_name, issue_md, commit_message=f"Add Jira issue {jira_issue.key}")

        # Create a new PR from the branch
        title = f"Sync Jira Issue {jira_issue.key}: {jira_issue.fields.summary}"
        body = f"This PR syncs the Jira issue {jira_issue.key} to GitHub for further discussion and development."
        repo.create_pull(title, body, branch_name, "main")

    def jira_issue_to_markdown(self, jira_issue):
        markdown = f"# Jira Issue {jira_issue.key}: {jira_issue.fields.summary}\n"
        markdown += f"## Description\n{jira_issue.fields.description}\n"
        markdown += "## Expected Output:\n"
        for exp_output in jira_issue.fields.customfield_10002:
            markdown += f"- {exp_output}\n"
        return markdown

# Example usage:
jira_auth = ("username", "api_token")
github_auth = {"login": "your_github_username", "password": "your_github_pat"}
sync_pipeline = JiraGithubSync("https://your_jira_server", jira_auth, github_auth)
sync_pipeline.sync_issue_to_pr("OPS-14")
```

## Unit Tests:

```python
import unittest
from unittest.mock import patch, MagicMock
from github import Github
from jira import JIRA

class TestJiraGithubSync(unittest.TestCase):
    def test_sync_issue_to_pr(self):
        jira_mock = MagicMock(spec=JIRA)
        jira_mock.issue.return_value = MagicMock(key="OPS-14", fields={"summary": "Implement Jira→GitHub sync pipeline",
                                                                         "description": "Ticket description",
                                                                         "customfield_10002": ["Code", "Tests", "Instructions"]})
        github_mock = MagicMock(spec=Github)
        github_mock.get_user.return_value = MagicMock(login="test_user")
        github_mock.get_repo.return_value = MagicMock(create_git_ref=MagicMock(), create_file=MagicMock(), create_pull=MagicMock())

        sync_