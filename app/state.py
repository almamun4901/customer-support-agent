from typing import TypedDict, Optional

class SupportState(TypedDict):
    userQuery: str
    category: str
    urgency: str
    sentiment: str
    kbContext: str
    answer: str
    escalate: bool
    ticketId: Optional[int]