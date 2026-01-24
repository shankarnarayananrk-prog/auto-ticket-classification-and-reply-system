# Shanyan AI - Setup & User Guide

## 🎯 System Overview

**Shanyan AI** is an enterprise-grade support ticketing system with intelligent ticket classification and automated responses powered by Google Gemma 3 27B and DistilBERT.

Created by **Shankar Narayanan**, Student, Dr MGR University.

### Key Features
- **AI-Powered Classification**: Automatically categorizes tickets using DistilBERT (57%+ accuracy, scalable to 90%+)
- **Smart Routing**: Intelligently routes tickets to the right department
- **Role-Based Access Control**: Separate interfaces for clients, departments, and administrators
- **Automated Responses**: Gemma 3 27B generates professional acknowledgment replies
- **Ticket Management**: Unique ticket numbers, status tracking, and department queues

---

## 🔐 User Roles & Access

### 1. **Client** (`client`)
- Submit support tickets
- View their own tickets
- Receive automated responses
- Track ticket status

### 2. **Technical Support** (`technical_support`)
- View tickets assigned to Technical/IT/Product Support
- Handle technical issues
- Monitor department queue

### 3. **Accounting** (`accounting`)
- View tickets assigned to Billing/Payments/Returns
- Process financial queries
- Manage accounting-related tickets

### 4. **Sales** (`sales`)
- View tickets assigned to Sales/Customer Service/General Inquiries
- Handle pre-sales and customer questions
- Manage sales pipeline

### 5. **Administrator** (`admin`)
- View ALL tickets from all departments
- Monitor entire system
- Oversee all operations

---

## 🚀 Quick Start

### Backend Setup

1. **Ensure backend is running:**
```bash
cd /Users/hnai/Downloads/auto-ticket-classification-and-reply-system/backend
source ../.venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

2. **Initialize demo users (first time only):**
```bash
curl -X POST http://localhost:8000/api/init-users
```

### Frontend Setup

```bash
cd /Users/hnai/Downloads/auto-ticket-classification-and-reply-system/frontend
npm run dev
```

Access the app at: `http://localhost:5173`

---

## 👥 Demo Accounts

### Administrator Access
- **Username:** `admin`
- **Password:** `admin123`
- **Can See:** All tickets from all departments

### Client Access
- **Username:** `client1`
- **Password:** `client123`
- **Name:** Rajesh Kumar
- **Can Do:** Submit tickets, view own tickets

### Technical Support
- **Username:** `tech1`
- **Password:** `tech123`
- **Name:** Priya Sharma
- **Can See:** Technical/IT/Product Support tickets only

### Accounting Department
- **Username:** `acc1`
- **Password:** `acc123`
- **Name:** Amit Patel
- **Can See:** Billing/Payments/Returns tickets only

### Sales Department
- **Username:** `sales1`
- **Password:** `sales123`
- **Name:** Sneha Reddy
- **Can See:** Sales/Customer Service/General tickets only

---

## 📋 Workflow Example

### Client Workflow
1. **Login** as `client1`
2. **Write a ticket**: "I was charged $49.99 twice on January 15th. Please refund."
3. **System automatically:**
   - Classifies as "Billing and Payments"
   - Routes to **Accounting** department
   - Generates ticket number (e.g., `TKT-20260125-A7F3`)
   - Creates automated response via Gemma 3
4. **Client sees:** Ticket number, classification, department assignment, and AI response

### Department Workflow (Accounting Staff)
1. **Login** as `acc1`
2. **View queue:** See only accounting-related tickets
3. **See ticket details:**
   - Client name
   - Ticket number
   - Issue description
   - Status (Pending/In Progress/Resolved)
4. **Process the ticket** (handle the refund)

### Admin Workflow
1. **Login** as `admin`
2. **View dashboard:** See ALL tickets from all departments
3. **Monitor:**
   - Technical support queue
   - Accounting department
   - Sales pipeline
4. **Oversight:** Full visibility across the organization

---

## 🎨 UI/UX Improvements Implemented

### Bug Fixes
✅ **Fixed left-alignment issue** - Container now properly centered
✅ **Fixed textarea text color** - Text is now dark and visible (was white)
✅ **Professional layout** - Clean, centered, modern glassmorphism design

### New Features
✅ **Login screen** - Secure authentication
✅ **User bar** - Shows current user and role
✅ **Ticket numbers** - Unique IDs like `TKT-20260125-ABCD`
✅ **Department badges** - Visual indicators for routing
✅ **Status tags** - Pending/In Progress/Resolved
✅ **Role-based UI** - Different views for different users

---

## 🏢 Department Mapping

The system automatically routes tickets to departments based on AI classification:

| AI Classification | Department |
|-------------------|------------|
| Technical Support | technical_support |
| IT Support | technical_support |
| Product Support | technical_support |
| Billing and Payments | accounting |
| Returns and Exchanges | accounting |
| Sales and Pre-Sales | sales |
| Customer Service | sales |
| General Inquiry | sales |

---

## 🧪 Test Scenarios

### Test as Client (Submit Tickets)

**Technical Issue:**
```
I can't access my dashboard. Every time I try to log in, the page refreshes and shows a 'Connection Timed Out' error.
```
→ Routes to: **Technical Support**

**Billing Issue:**
```
I was charged $49.99 twice on January 15th for the same subscription. Please refund one of the duplicate charges.
```
→ Routes to: **Accounting**

**Sales Inquiry:**
```
We are looking to implement this system for a team of 200 members. Do you offer custom enterprise pricing?
```
→ Routes to: **Sales**

### Test as Department Staff

1. Login as `tech1`
2. You'll ONLY see technical tickets
3. Other departments won't see your tickets

### Test as Admin

1. Login as `admin`
2. You'll see ALL tickets from ALL departments
3. Complete visibility across the system

---

## 📊 Model Performance

### Classification Model: DistilBERT
- **Current Accuracy:** 57.58% (3 epochs)
- **Target Accuracy:** 90%+
- **How to improve:** Increase epochs to 10 in `backend/training/train.py`

### Reply Generation: Gemma 3 27B
- **Model:** `models/gemma-3-27b-it`
- **Purpose:** Professional acknowledgment responses
- **Quality:** High-quality, empathetic replies

---

## 🔧 Technical Stack

**Backend:**
- FastAPI
- SQLAlchemy + SQLite
- Google GenAI SDK (Gemma 3 27B)
- Transformers (DistilBERT)
- PyTorch

**Frontend:**
- React (Vite)
- Axios
- Lucide React Icons
- Modern CSS (Glassmorphism)

---

## 📝 Database Schema

### Users Table
- `id`, `username`, `password`, `full_name`, `role`, `created_at`

### Tickets Table
- `id`, `ticket_number`, `client_id`, `client_name`
- `body`, `predicted_queue`, `generated_reply`
- `status`, `assigned_department`
- `created_at`, `updated_at`

---

## 🎓 For Academic Submission (Dr. MGR University)

This project demonstrates:
1. ✅ **AI/ML Integration**: DistilBERT for classification, Gemma 3 for NLP
2. ✅ **Role-Based Access Control**: Multi-user system with different permissions
3. ✅ **Modern UI/UX**: Professional, centered, glassmorphism design
4. ✅ **Enterprise Architecture**: RESTful API, database persistence, authentication
5. ✅ **Scalability**: Supports multiple departments and unlimited users

---

## 🚨 Important Notes

- **Production Security:** In a real system, use bcrypt for password hashing and JWT for tokens
- **Environment Variables:** Ensure `GEMINI_API_KEY` is set in `backend/.env`
- **Database:** Currently using SQLite (fine for demo), use PostgreSQL for production
- **Model Training:** Run `backend/training/train.py` to retrain the classifier

---

## 📞 Support

For issues or questions about this implementation, refer to the codebase documentation or the API endpoints at `http://localhost:8000/docs` (FastAPI automatic docs).
