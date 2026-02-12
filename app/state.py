from typing import TypedDict, Optional

class TicketState(TypedDict):
    userQuery: str
    category: str
    urgency: str
    sentiment: str
    kbContext: str
    answer: str
    escalate: bool
    ticketId: Optional[int]