from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from app.state import SupportState
from app.llm import get_llm
from app.kb import search_kb
from app.tickets import create_ticket, update_ticket

class Triage(BaseModel):
    category: str
    urgency: str
    sentiment: str

def triage(state: SupportState):
    llm = get_llm(temp = 0).with_structured_output(Triage)
    
    result = llm.invoke(f"""
    Analyze this support ticket and determine the category, urgency, and sentiment.
    
    Ticket: {state['userQuery']}
    
    Return a JSON object with the following fields:
    - category: The category of the ticket (e.g., billing, technical, sales, refund, general)
    - urgency: The urgency of the ticket (e.g., low, medium, high)
    - sentiment: The sentiment of the ticket (e.g., positive, negative, neutral)
    """)
    return result.model_dump()

def retrieve(state: SupportState):
    context = search_kb(state['userQuery'])
    return {"kbContext": context}


