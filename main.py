from flask import Flask
import os
import base64
import google.generativeai as genai
import smtplib
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables from .env (for local development)
load_dotenv()

# Decode the service account JSON from the environment variable
json_data = base64.b64decode(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
service_account_path = "service_account.json"  # Path to save the decoded JSON
with open(service_account_path, "wb") as f:
    f.write(json_data)

# Initialize Flask app
app = Flask(__name__)

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
credentials = Credentials.from_service_account_file(service_account_path, scopes=SCOPES)
SHEET_ID = os.getenv("SHEET_ID")  # Google Sheet ID from environment variables
RANGE_NAME = os.getenv("RANGE_NAME", "Form Responses 1")  # Default range name

# Gmail setup
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def get_user_data(data):
    """Extract user data from the form submission."""
    if data:
        user_data = {
            "timestamp": data[0],
            "first_name": data[1],
            "last_name": data[2],
            "email": data[3],
            "country": data[4],
            "location": data[5],
            "project_type": data[6],
            "service_category": data[7],
            "website": data[8],
            "additional_info": data[9],
            "budget": data[10],
        }
        return user_data
    return None

def generate_email_response(user_data, client_email):
    """Generate and send a professional email response using AI."""
    genai.configure(api_key=os.getenv("GENERATIVE_AI_API_KEY"))  # API key from environment variables
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Prepare the input content from user data
    input_content = f"""
        Client First Name: {user_data['first_name']}
        Client Last Name: {user_data['last_name']}
        Client Email: {user_data['email']}
        Client Country: {user_data['country']}
        Client Location: {user_data['location']}
        Project Type: {user_data['project_type']}
        Service Category: {user_data['service_category']}
        Client Website: {user_data['website']}
        Additional Information: {user_data['additional_info']}
        Budget: {user_data['budget']}
    """

    # AI Prompt to generate a structured email
    prompt = f"""
        Write a professional email response based on the following client details:
        {input_content}
        The email should:
        - Express gratitude for their inquiry.
        - Introduce yourself briefly.
        - Summarize their requirements clearly.
        - Propose a next step for further discussion.
        - Be polite, warm, and professional.
        Format the email as follows:
        - Salutation with the client's full name.
        - Introduction and summary of their project details.
        - Closing remarks with a professional signature.
    """

    try:
        # Generate email content using AI
        response = model.generate_content(prompt)
        generated_email = response.text.strip()

        # Append your signature
        signature = """
        Best regards,
        Jesna
        Project Manager
        XYZ Solutions
        """
        full_message = f"{generated_email}\n\n{signature}"

        # Send the generated email
        send_email(client_email, full_message)

    except Exception as e:
        print(f"Error generating email response: {e}")

def get_latest_form_data():
    """Fetch the latest form submission from Google Sheets."""
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    rows = result.get('values', [])
    if rows:
        return rows[-1]  # Return the latest submission
    return None

def send_email(client_email, message):
    """Send the generated email response to the client."""
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=GMAIL_USER, password=GMAIL_PASSWORD)
        connection.sendmail(
            from_addr=GMAIL_USER,
            to_addrs=client_email,
            msg=f"Subject: Project Inquiry Response\n\n{message}".encode("utf-8")
        )

@app.route("/")
def index():
    """This route will trigger the logic to fetch form data and send email."""
    latest_submission = get_latest_form_data()
    if latest_submission:
        user_data = get_user_data(latest_submission)
        if user_data:
            generate_email_response(user_data, user_data['email'])  # Generate and send the email
        return "Email sent!"
    else:
        return "No new data found."

if __name__ == "__main__":
    app.run(debug=True)
