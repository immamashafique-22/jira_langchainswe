from services.jira import JiraService
from services.github import GitHubService
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

jira_service = JiraService()
github_service = GitHubService(os.environ["GITHUB_TOKEN"], os.environ["GITHUB_REPO"])

# ---------- Create a new Jira ticket ----------
new_ticket = jira_service.create_ticket(
    project=os.environ["JIRA_PROJECT"],
    summary="Implement ticket sync with GitHub",
    description="This ticket will be pushed to GitHub as a .md file and linked with a PR.",
)
print(f"Created new Jira ticket: {new_ticket.key}")

# ---------- Update the Jira ticket ----------
updated_ticket = jira_service.update_ticket(
    issue_key=new_ticket.key,
    fields={"summary": "Implement Jira→GitHub sync pipeline"},
    comment="Updated summary before pushing to GitHub.",
)
print(f"Updated Jira ticket: {updated_ticket.key}")

# ---------- Fetch tickets from Jira ----------
tickets = jira_service.fetch_tickets()
print("\nFetched Tickets:")
for t in tickets:
    print(f"{t['key']}: {t['summary']} (Status: {t['status']})")

# ---------- Push tickets to GitHub ----------
for ticket in tickets:
    branch_name = f"ticket-{ticket['key']}"
    file_name = f"tickets/{ticket['key']}.md"
    file_content = f"# {ticket['summary']}\n\n{ticket['description']}\n\nStatus: {ticket['status']}"

    # Create branch (ignore if exists)
    try:
        github_service.create_branch(branch_name)
    except Exception as e:
        print(f"Branch may already exist: {e}")

    # Push or update file in GitHub
    github_service.push_file(
        branch_name,
        file_name,
        file_content,
        commit_message=f"Add/Update Jira ticket {ticket['key']}",
    )

    # Create a PR
    pr = github_service.create_pull_request(
        title=f"Sync Jira Ticket {ticket['key']}",
        body=f"This PR syncs Jira ticket {ticket['key']} with GitHub.\n\n{ticket['summary']}",
        branch_name=branch_name,
    )
    print(f"Created GitHub PR for {ticket['key']}: {pr.html_url}")
