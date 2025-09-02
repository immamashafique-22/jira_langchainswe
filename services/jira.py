from jira import JIRA
from config import JIRA_EMAIL, JIRA_API_TOKEN, JIRA_SERVER, PROJECT_KEY


class JiraService:
    def __init__(self):
        options = {"server": JIRA_SERVER}
        self.jira = JIRA(options=options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

    def fetch_tickets(self, jql=None, max_results=50):
        if not jql:
            jql = f"project={PROJECT_KEY} AND status!=Done"
        issues = self.jira.search_issues(jql, maxResults=max_results)
        tickets = []
        for issue in issues:
            tickets.append(
                {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "description": issue.fields.description or "",
                    "status": issue.fields.status.name,
                    "assignee": (
                        issue.fields.assignee.displayName
                        if issue.fields.assignee
                        else None
                    ),
                }
            )
        return tickets

    def create_ticket(
        self,
        summary,
        description,
        issue_type="Task",
        assignee=None,
        priority=None,
        project_key=PROJECT_KEY,
    ):
        issue_dict = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
        new_issue = self.jira.create_issue(fields=issue_dict)

        if assignee:
            try:
                self.jira.assign_issue(new_issue.key, assignee)
            except Exception as e:
                print("Assignee update skipped:", e)

        if priority:
            try:
                new_issue.update(fields={"priority": {"name": priority}})
            except Exception as e:
                print("Priority update skipped:", e)

        return new_issue.key

    def update_ticket(self, ticket_key, status=None, assignee=None, comment=None):
        issue = self.jira.issue(ticket_key)

        if status:
            transitions = {t["name"]: t["id"] for t in self.jira.transitions(issue)}
            if status in transitions:
                self.jira.transition_issue(issue, transitions[status])

        if assignee:
            try:
                self.jira.assign_issue(issue.key, assignee)
            except Exception as e:
                print("Assignee update skipped:", e)

        if comment:
            self.jira.add_comment(issue.key, comment)

        return True
