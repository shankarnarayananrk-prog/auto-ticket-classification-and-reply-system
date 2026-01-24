from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .db import get_db
from .models import Ticket, User, UserRole, TicketStatus
from .services.classifier import TicketClassifierService
from .services.gemini import GeminiService
from datetime import datetime
import random
import string

router = APIRouter()
classifier_service = TicketClassifierService()
gemini_service = GeminiService()

# Department mapping
DEPARTMENT_MAPPING = {
    "Technical Support": "technical_support",
    "IT Support": "technical_support",
    "Product Support": "technical_support",
    "Billing and Payments": "accounting",
    "Returns and Exchanges": "accounting",
    "Sales and Pre-Sales": "sales",
    "Customer Service": "sales",
    "General Inquiry": "sales"
}

def generate_ticket_number():
    """Generate a unique ticket number like TKT-20260125-ABCD"""
    date_str = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TKT-{date_str}-{random_str}"

# Request/Response Models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    user_id: int
    username: str
    full_name: str
    role: str
    token: str

class TicketRequest(BaseModel):
    description: str
    client_id: int
    client_name: str

class TicketResponse(BaseModel):
    ticket_number: str
    queue: str
    auto_reply: str
    assigned_department: str

class TicketListItem(BaseModel):
    id: int
    ticket_number: str
    client_name: str
    body: str
    predicted_queue: str
    assigned_department: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Authentication
@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user or user.password != request.password:  # In production, use hashing!
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Simple token (in production, use JWT)
    token = f"token_{user.id}_{user.role}"
    
    return LoginResponse(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        token=token
    )

# Create ticket
@router.post("/predict", response_model=TicketResponse)
async def predict_ticket(request: TicketRequest, db: Session = Depends(get_db)):
    try:
        # 1. Predict Queue
        predicted_queue = classifier_service.predict(request.description)
        
        # 2. Map to department
        assigned_department = DEPARTMENT_MAPPING.get(predicted_queue, "sales")
        
        # 3. Generate ticket number
        ticket_number = generate_ticket_number()
        
        # 4. Generate Reply using SN AI Bot
        generated_reply = gemini_service.generate_reply(
            request.description, 
            predicted_queue, 
            ticket_number, 
            request.client_name
        )
        
        # 5. Store in DB
        db_ticket = Ticket(
            ticket_number=ticket_number,
            client_id=request.client_id,
            client_name=request.client_name,
            body=request.description,
            predicted_queue=predicted_queue,
            generated_reply=generated_reply,
            assigned_department=assigned_department,
            status=TicketStatus.PENDING
        )
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        
        return TicketResponse(
            ticket_number=ticket_number,
            queue=predicted_queue,
            auto_reply=generated_reply,
            assigned_department=assigned_department
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get tickets based on role
@router.get("/tickets/{role}/{user_id}")
async def get_tickets(role: str, user_id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(Ticket)
        
        if role == "admin":
            # Admin sees all tickets
            tickets = query.order_by(Ticket.created_at.desc()).all()
        elif role == "client":
            # Client sees only their tickets
            tickets = query.filter(Ticket.client_id == user_id).order_by(Ticket.created_at.desc()).all()
        elif role in ["technical_support", "accounting", "sales"]:
            # Department staff sees only their department's tickets
            tickets = query.filter(Ticket.assigned_department == role).order_by(Ticket.created_at.desc()).all()
        else:
            raise HTTPException(status_code=403, detail="Invalid role")
        
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize default users (for development)
@router.post("/init-users")
async def initialize_users(db: Session = Depends(get_db)):
    """Create default users if they don't exist"""
    default_users = [
        {"username": "admin", "password": "admin123", "full_name": "System Administrator", "role": UserRole.ADMIN},
        {"username": "client1", "password": "client123", "full_name": "Rajesh Kumar", "role": UserRole.CLIENT},
        {"username": "tech1", "password": "tech123", "full_name": "Priya Sharma", "role": UserRole.TECHNICAL_SUPPORT},
        {"username": "acc1", "password": "acc123", "full_name": "Amit Patel", "role": UserRole.ACCOUNTING},
        {"username": "sales1", "password": "sales123", "full_name": "Sneha Reddy", "role": UserRole.SALES},
    ]
    
    created = []
    for user_data in default_users:
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing:
            user = User(**user_data)
            db.add(user)
            created.append(user_data["username"])
    
    db.commit()
    return {"message": "Users initialized", "created": created}
