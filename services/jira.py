from jira import JIRA
import os


class JiraService:
    def __init__(self):
        self.jira = JIRA(
            server=os.getenv("JIRA_URL"),
            basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")),
        )

    def fetch_tickets(self, jql=None):
        if not jql:
            jql = f'project={os.getenv("JIRA_PROJECT", "OPS")} ORDER BY created DESC'
        issues = self.jira.search_issues(jql, maxResults=10)
        return [
            {
                "key": i.key,
                "summary": i.fields.summary,
                "description": i.fields.description,
                "status": i.fields.status.name,
            }
            for i in issues
        ]

    def create_ticket(self, project, summary, description):
        issue = self.jira.create_issue(
            project=project,
            summary=summary,
            description=description,
            issuetype={"name": "Task"},
        )
        return issue

    def update_ticket(self, issue_key, fields=None, comment=None):
        issue = self.jira.issue(issue_key)
        if fields:
            issue.update(fields=fields)
        if comment:
            self.jira.add_comment(issue, comment)
        return issue
