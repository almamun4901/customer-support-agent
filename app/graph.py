from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from app.state import SupportState
from app.llm import get_llm
from app.kb import retrieve_context
from app.tickets import create_ticket

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
    context = retrieve_context(state['userQuery'])
    return {"kbContext": context}

def escalationLogic(state: SupportState):
    escalate = (
        state['urgency'] == 'high' or 
        state['sentiment'] == 'negative' or
        (state['category'] == 'billing' and (state['urgency'] == 'high' or state['sentiment'] == 'negative'))
    )
    return {"escalate": escalate}

def generate_response(state: SupportState):
    llm = get_llm(temp = 0.7)
    
    response = llm.invoke(f"""
    Answer this support ticket based on the following context:
    
    Ticket: {state['userQuery']}
    Context: {state['kbContext']}
    
    Return a JSON object with the following fields:
    - answer: The answer to the ticket
    """)
    return {"answer": response.content}

def createTicket(state: SupportState):
    ticket_id = create_ticket(state)
    return {"ticketId": ticket_id}

def build_graph():
    workflow = StateGraph(SupportState)
    
    workflow.add_node("triage", triage)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("escalationLogic", escalationLogic)
    workflow.add_node("generate_response", generate_response)
    workflow.add_node("createTicket", createTicket)
    
    workflow.add_edge(START, "triage")
    workflow.add_edge("triage", "retrieve")
    workflow.add_edge("retrieve", "escalationLogic")
    workflow.add_edge("escalationLogic", "generate_response")
    workflow.add_edge("generate_response", "createTicket")
    workflow.add_edge("createTicket", END)
    
    return workflow.compile()

