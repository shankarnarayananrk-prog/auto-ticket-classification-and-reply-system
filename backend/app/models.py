from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from datetime import datetime
from .db import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CLIENT = "client"
    TECHNICAL_SUPPORT = "technical_support"
    ACCOUNTING = "accounting"
    SALES = "sales"

class TicketStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)  # In production, hash this!
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, unique=True, nullable=False, index=True)
    client_id = Column(Integer, nullable=False)
    client_name = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    predicted_queue = Column(String, index=True)
    generated_reply = Column(Text)
    status = Column(Enum(TicketStatus), default=TicketStatus.PENDING)
    assigned_department = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
