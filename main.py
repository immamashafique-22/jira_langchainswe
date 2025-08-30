from services.jira import JiraService
from services.ai_service import AIService
from config import PROJECT_KEY

# initializing Jira
jira_service = JiraService()
tickets = jira_service.fetch_tickets(jql=f"project={PROJECT_KEY} AND status!=Done")

print("Fetched Tickets:")
for t in tickets:
    print(f"{t['key']}: {t['summary']} (Status: {t['status']})")

docs = [f"{t['summary']} {t['description']}" for t in tickets]

# initializing AI service (Cohere)
ai_service = AIService(docs)

query = "Summarize key issues and suggest tickets to prioritize."
summary = ai_service.get_summary(query)
print("\n=== AI Summary ===\n", summary)

# creating new ticket
new_ticket_key = jira_service.create_ticket(
    summary="Test Ticket via API",
    description="This ticket was created",
)
print("\nNew Ticket Created:", new_ticket_key)

# updating ticket
if tickets:
    jira_service.update_ticket(
        ticket_key=tickets[0]["key"],
        status="In Progress",
        comment="Updated status via API.",
    )
    print(f"Updated Ticket: {tickets[0]['key']}")
