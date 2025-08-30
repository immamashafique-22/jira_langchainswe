# test_jira.py
from jira import JIRA
from config import JIRA_EMAIL, JIRA_API_TOKEN, JIRA_SERVER


def test_jira_connection(project_key="TEST"):
    try:
        jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
        issues = jira.search_issues(f"project={project_key}", maxResults=5)

        print(f"Tickets fetched from project {project_key}: {len(issues)}\n")
        for i, t in enumerate(issues, 1):
            print(f"{i}. {t.key} - {t.fields.summary}")

        if not issues:
            print("No tickets found. Check project key or Jira permissions.")
        else:
            print("\nJira connection and fetch test passed!")

    except Exception as e:
        print("Error connecting to Jira:", e)


if __name__ == "__main__":
    # Replace "TEST" with your actual Jira project key
    test_jira_connection(project_key="TEST")
