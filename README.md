# AI-Powered Customer Support Ticket Automation System

An end-to-end AI system for automating customer support ticket triaging and acknowledgement. It uses a fine-tuned **DistilBERT** model for ticket classification and **Google's Gemma 3 27B** model (via Gemini API) for generating empathetic, professional replies.

## 🚀 Features

- **Automated Classification**: Categorizes incoming tickets into 10 different departments (Technical Support, Billing, Sales, etc.) using a fine-tuned DistilBERT transformer model.
- **AI-Powered Replies**: Automatically generates polite acknowledgement responses using Gemma 3 27B (`gemma-3-27b-it`).
- **Persistence**: Stores all processed tickets and AI responses in a SQLite database.
- **Modern UI**: Clean, responsive frontend built with React and Vite.

## 🛠️ Tech Stack

| Layer                    | Technology                                            |
| ------------------------ | ----------------------------------------------------- |
| **Backend**              | FastAPI (Python)                                      |
| **Classification Model** | DistilBERT (fine-tuned via Hugging Face Transformers) |
| **Reply Generation**     | Gemma 3 27B via Gemini API                            |
| **Database**             | SQLite with SQLAlchemy ORM                            |
| **Frontend**             | React, Vite, Lucide-React                             |
| **Styling**              | Modern CSS3                                           |

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   React UI      │ ──▶  │  FastAPI Server │ ──▶  │   SQLite DB     │
│   (Vite)        │      │                 │      │                 │
└─────────────────┘      └────────┬────────┘      └─────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
          ┌─────────────────┐         ┌─────────────────┐
          │ DistilBERT      │         │ Gemma 3 27B     │
          │ (Classification)│         │ (Reply Gen)     │
          └─────────────────┘         └─────────────────┘
```

1. **Frontend (React)**: Collects ticket input and displays classification & generated reply.
2. **FastAPI Backend**: Orchestrates the workflow.
3. **DistilBERT Classifier**: Fine-tuned transformer model that predicts the correct department.
4. **Gemma 3 27B**: Takes the ticket text and category to draft a professional response.
5. **Database**: Records every interaction for audit and history purposes.

## 📋 Prerequisites

- Python 3.10+
- Node.js 16+
- Gemini API Key (for accessing Gemma models)

## 🔑 Getting Your Gemini API Key

To use the Gemma 3 27B model for generating replies, you need a Gemini API key from Google AI Studio:

1. **Visit Google AI Studio**: Go to [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)

2. **Sign in**: Use your Google account to sign in.

3. **Create API Key**: Click the **"Create API key"** button in the top right corner.

4. **Select Project**: Choose an existing Google Cloud project or create a new one.

5. **Copy Your Key**: Once generated, copy the API key immediately (it starts with `AIza...`).

6. **Secure Your Key**: Store it safely - you won't be able to see it again in the console.

> ⚠️ **Important**: Keep your API key secure. Never commit it to version control or share it publicly.

## ⚙️ Setup Instructions

### 1. Backend Setup

1. Navigate to the `backend` folder:

   ```bash
   cd backend
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `backend` folder with your API key:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=sqlite:///./tickets.db
   ```

4. (Optional) Train the DistilBERT model from scratch:

   ```bash
   python training/train.py
   ```

   > Note: A pre-trained model is already included in `training/models/fine_tuned_bert/`

5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend will run at `http://localhost:8000`

### 2. Frontend Setup

1. Navigate to the `frontend` folder:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will run at `http://localhost:5173`

### 3. Quick Start (Both Services)

Use the provided script to start both backend and frontend:

```bash
./start.sh
```

## 📊 Model Details

### Classification Model (DistilBERT)

- **Base Model**: `distilbert-base-uncased`
- **Training Data**: [Tobi-Bueck/customer-support-tickets](https://huggingface.co/datasets/Tobi-Bueck/customer-support-tickets) from Hugging Face
- **Fine-tuning**: 3 epochs with batch size 16
- **Categories**: Top 10 support categories including:
  - Technical Support
  - Billing Inquiry
  - Sales and Pre-Sales
  - IT Support
  - And more...

### Reply Generation Model (Gemma)

- **Model**: `gemma-3-27b-it` (instruction-tuned)
- **Provider**: Google AI via Gemini API
- **Purpose**: Generates professional, empathetic acknowledgement responses

## 📁 Project Structure

```
auto-ticket-classification-and-reply-system/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models/              # Database models
│   │   └── services/
│   │       ├── classifier.py    # DistilBERT classification
│   │       └── gemini.py        # Gemma reply generation
│   ├── training/
│   │   ├── train.py             # Model training script
│   │   ├── models/              # Saved model weights
│   │   └── label_encoder.pkl    # Category encoder
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   └── components/          # UI components
│   ├── package.json
│   └── vite.config.js
├── start.sh                      # Quick start script
└── README.md
```

## 🎓 Academic Context

**Institution**: Dr. MGR University  
**Project**: AI-Powered Ticket Automation

---

_Developed for research and academic demonstration purposes._
