import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

# Load .env from backend directory
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        self.client = genai.Client(api_key=api_key)

    def generate_reply(self, ticket_text, predicted_queue, ticket_number, client_name):
        # Determine the appropriate tone based on the ticket category
        if predicted_queue in ["Sales and Pre-Sales", "General Inquiry"]:
            tone_instruction = """
IMPORTANT: This is a SALES/INQUIRY ticket. The customer is interested in our products or services.
Your response should be:
- Warm, enthusiastic, and welcoming
- Express gratitude and excitement about their interest
- Show eagerness to help them with their purchase/inquiry
- DO NOT apologize - there is no issue or problem to apologize for
- Use positive language like "We're thrilled", "We're excited to help", "Great choice"
"""
            subject_type = "inquiry"
        elif predicted_queue in ["Technical Support", "IT Support", "Product Support"]:
            tone_instruction = """
IMPORTANT: This is a TECHNICAL SUPPORT ticket. The customer has a problem that needs solving.
Your response should be:
- Professional and empathetic
- Acknowledge their issue and express understanding
- Apologize for any inconvenience they're experiencing
- Assure them the issue will be investigated and resolved
"""
            subject_type = "support request"
        elif predicted_queue in ["Billing and Payments", "Returns and Exchanges"]:
            tone_instruction = """
IMPORTANT: This is a BILLING/RETURNS ticket. The customer has a financial or return-related concern.
Your response should be:
- Professional, reassuring, and understanding
- Acknowledge their concern
- Express appropriate empathy if it's a problem
- Assure them the matter will be reviewed promptly
"""
            subject_type = "request"
        else:
            tone_instruction = """
Your response should be professional, helpful, and appropriately match the customer's message tone.
If they're reporting a problem, be empathetic and apologize.
If they're making an inquiry or showing interest, be welcoming and enthusiastic.
"""
            subject_type = "request"

        prompt = f"""
You are Shanyan AI Bot, a customer support assistant for Shanyan AI company.

Ticket Number: {ticket_number}
Ticket Category: {predicted_queue}
Customer Name: {client_name}
Customer Message: {ticket_text}

{tone_instruction}

Write a professional acknowledgement reply with this format:

Subject: Regarding your recent {predicted_queue.lower()} {subject_type} - [Ticket Number - {ticket_number}]

Dear {client_name},

[Write 2-3 sentences that appropriately respond to their message based on the tone instruction above. Summarize what they're asking about and express the appropriate sentiment.]

[Write 1-2 sentences about next steps - either how you'll help them with their purchase/inquiry OR how you'll investigate their issue.]

Sincerely,
Shanyan AI Bot
Shanyan AI Customer Support

CRITICAL: Match your tone to the ticket category. Sales inquiries should be enthusiastic. Support issues should be empathetic with apologies.
"""
        response = self.client.models.generate_content(
            model='gemma-3-27b-it',
            contents=prompt
        )
        return response.text.strip()
