from services.jira import JiraService
from services.ai_service import LangChainAIService
from config import PROJECT_KEY

jira_service = JiraService()
tickets = jira_service.fetch_tickets(jql=f"project={PROJECT_KEY} AND status!=Done")

print("Fetched Tickets:")
for t in tickets:
    print(f"{t['key']}: {t['summary']} (Status: {t['status']})")

docs = [f"{t['summary']} {t['description']}" for t in tickets]

ai_service = LangChainAIService(docs)

summary = ai_service.summarize_tickets()
print("\n=== AI Summary (LangChain SWE) ===\n", summary)

# Create a test ticket
new_ticket_key = jira_service.create_ticket(
    summary="Test Ticket via LangChain SWE",
    description="This ticket was created via LangChain SWE pipeline",
)
print("\nNew Ticket Created:", new_ticket_key)

# Update first ticket
if tickets:
    jira_service.update_ticket(
        ticket_key=tickets[0]["key"],
        status="In Progress",
        comment="Updated status via LangChain SWE pipeline.",
    )
    print(f"Updated Ticket: {tickets[0]['key']}")
