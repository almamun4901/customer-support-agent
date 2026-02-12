from datetime import datetime
from typing import Optional

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Text,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String(50), nullable=False)
    urgency = Column(String(20), nullable=False)
    sentiment = Column(String(20), nullable=False)
    status = Column(String(20), default="open")
    user_query = Column(Text, nullable=False)
    agent_summary = Column(Text, nullable=True)


# Initialize DB
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


def create_ticket(state: dict) -> int:
    """
    Creates a support ticket from state.
    Returns ticket ID.
    """
    session = SessionLocal()

    ticket = Ticket(
        category=state.get("category", "general"),
        urgency=state.get("urgency", "medium"),
        sentiment=state.get("sentiment", "neutral"),
        user_query=state.get("userQuery"),
        agent_summary=state.get("answer"),
    )

    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    session.close()

    return ticket.id


def get_ticket(ticket_id: int) -> Optional[Ticket]:
    session = SessionLocal()
    ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
    session.close()
    return ticket
