# Test cases
Sure! Here is the code, tests, and instructions based on the provided Jira ticket:

## Code Implementation:

```python
import jira
import github
from datetime import datetime

class JiraGithubSync:
    def __init__(self, jira_server, jira_auth, github_auth):
        self.jira_server = jira_server
        self.jira_client = jira.JIRA(basic_auth=jira_auth, options={'server': jira_server})
        self.github_client = github.Github(github_auth)

    def sync_issue_to_pr(self, jira_issue_id):
        jira_issue = self.jira_client.issue(jira_issue_id)
        repo_name = f"project-{jira_issue.key}"
        repo = self.github_client.get_repo(repo_name)

        # Create a new branch and commit the Jira issue as a Markdown file
        branch_name = f"jira-issue-{jira_issue.key}"
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=repo.get_commits()[0].sha)
        issue_md = self.jira_issue_to_markdown(jira_issue)
        repo.create_file(f"{jira_issue.key}.md", "Jira Issue Sync", issue_md)

        # Create a Pull Request from the new branch
        title = f"Sync Jira Issue {jira_issue.key}: {jira_issue.fields.summary}"
        body = f"This PR syncs the Jira issue {jira_issue.key} to GitHub.\n\n{issue_md}"
        base_branch = "main"
        pr = repo.create_pull(title, body, branch_name, base_branch)
        print(f"Created PR #{pr.number}: {pr.title}")

    def jira_issue_to_markdown(self, jira_issue):
        markdown = f"# Jira Issue {jira_issue.key}: {jira_issue.fields.summary}\n"
        markdown += f"## Description\n{jira_issue.fields.description}\n"
        markdown += "## Details:\n"
        markdown += self.format_issue_details(jira_issue)
        return markdown

    def format_issue_details(self, jira_issue):
        details = ['**Type**: {type}',
                   '**Status**: {status}',
                   '**Priority**: {priority}',
                   '**Assignee**: {assignee}',
                   '**Created**: {created}',
                   '**Updated**: {updated}']
        formatted_details = []
        for detail in details:
            info = detail.format(type=jira_issue.fields.issuetype.name,
                                status=jira_issue.fields.status.name,
                                priority=jira_issue.fields.priority.name if jira_issue.fields.priority else None,
                                assignee=jira_issue.fields.assignee.name if jira_issue.fields.assignee else None,
                                created=jira_issue.fields.created,
                                updated=jira_issue.fields.updated)
            formatted_details.append(info)
        return '\n'.join(formatted_details)

# Example usage:
jira_server = "https://your-jira-server.com"
jira_auth = ("your-jira-username", "your-jira-api-token")
github_auth = github.GithubAuthentication(type="token", token="your-github-access-token")
sync_tool = JiraGithubSync(jira_server, jira_auth, github_