from services.jira import JiraService
from services.ai_service import LangChainAIService
from services.github import GitHubService
from config import PROJECT_KEY
import os

# ------------------------------
# Jira Setup
# ------------------------------
jira_service = JiraService()
tickets = jira_service.fetch_tickets(jql=f"project={PROJECT_KEY} AND status!=Done")

print("Fetched Tickets:")
for t in tickets:
    print(f"{t['key']}: {t['summary']} (Status: {t['status']})")

docs = [f"{t['summary']} {t['description']}" for t in tickets]

# ------------------------------
# AI Service Setup
# ------------------------------
ai_service = LangChainAIService(docs)

summary = ai_service.summarize_tickets()
print("\n=== AI Summary (LangChain SWE) ===\n", summary)

# ------------------------------
# GitHub Setup
# ------------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("GITHUB_REPO")

if not GITHUB_TOKEN or not REPO_NAME:
    raise ValueError("Missing GitHub credentials in environment variables")

github_service = GitHubService(GITHUB_TOKEN, REPO_NAME)

# ------------------------------
# Create/Update Tickets and PRs
# ------------------------------

# 1️⃣ Create a test Jira ticket
new_ticket_key = jira_service.create_ticket(
    summary="Test Ticket via LangChain SWE",
    description="This ticket was created via LangChain SWE pipeline",
)
print("\nNew Ticket Created:", new_ticket_key)

# 2️⃣ Update first ticket and generate PR
if tickets:
    first_ticket = tickets[0]

    jira_service.update_ticket(
        ticket_key=first_ticket["key"],
        status="In Progress",
        comment="Updated status via LangChain SWE pipeline.",
    )
    print(f"Updated Ticket: {first_ticket['key']}")

    pr_suggestion = ai_service.generate_pr_suggestions(first_ticket)

    branch_name = pr_suggestion.get("branch", f"{first_ticket['key']}-branch")
    pr_title = pr_suggestion.get("title", f"PR for {first_ticket['key']}")
    pr_body = pr_suggestion.get("description", first_ticket["summary"])
    file_updates = pr_suggestion.get(
        "files", {"README.md": f"# Update for {first_ticket['key']}"}
    )

    # Create branch in GitHub
    github_service.create_branch(branch_name)

    # Push files
    for path, content in file_updates.items():
        github_service.push_file(
            branch_name,
            path,
            content,
            commit_message=f"Update for {first_ticket['key']}",
        )

    # Create PR
    pr = github_service.create_pull_request(pr_title, pr_body, branch_name)
    print(f"Created GitHub PR: {pr.html_url}")
