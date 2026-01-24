# AI-Powered Customer Support Ticket Automation System

This project is an end-to-end AI system built for automating customer support ticket triaging and acknowledgement. It uses a Deep Learning (LSTM) model for ticket classification and Google's Gemini API for generating empathetic, professional replies.

## 🚀 Features

- **Automated Classification**: Categorizes incoming tickets into 10 different departments (Technical Support, Billing, etc.) using an LSTM model.
- **AI-Powered Replies**: Automatically generates polite acknowledgement responses using Gemini 1.5 Flash.
- **Persistence**: Stores all processed tickets and AI responses in a SQLite database.
- **Modern UI**: Clean, responsive frontend built with React and Vite.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **ML/NLP**: PyTorch, Scikit-learn, Hugging Face Datasets
- **Large Language Model**: Google Gemini API
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: React, Vite, Lucide-React
- **Styling**: Modern CSS3

## 🏗️ Architecture

1. **Frontend (React)**: Collects ticket input and displays classification & generated reply.
2. **FastAPI Backend**: Orchestrates the workflow.
3. **LSTM Classifier**: Processes text and predicts the correct department.
4. **Gemini API**: Takes the ticket text and category to draft a response.
5. **Database**: Records every interaction for audit and history purposes.

## 📋 Prerequisites

- Python 3.10+
- Node.js 16+
- Google Gemini API Key

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
3. Create a `.env` file in the `backend` folder and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   DATABASE_URL=sqlite:///./tickets.db
   ```
4. Train the LSTM model:
   ```bash
   python training/train.py
   ```
5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

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

## 📊 Model Evaluation

The LSTM model is trained on the `Tobi-Bueck/customer-support-tickets` dataset from Hugging Face.
- **Accuracy**: ~37% (Base model for demonstration)
- **Classes**: Top 10 support categories including Billing, Technical Support, and IT Support.

## 🎓 Academic Context

**Institution**: Dr. MGR University
**Project**: AI-Powered Ticket Automation
**Author**: [Your Name/Team]

---
*Developed for research and academic demonstration purposes.*
