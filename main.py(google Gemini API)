from flask import Flask, request, jsonify
import os
import base64
import google.generativeai as genai
import smtplib
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Decode the service account JSON from the environment variable
# This section ensures the service account key is accessible for the Google Generative AI API
json_data = base64.b64decode(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
service_account_path = "service_account.json"  # Path to save the decoded JSON
with open(service_account_path, "wb") as f:
    f.write(json_data)

# Initialize Flask app
# This app listens for incoming requests from external sources (e.g., a webhook)
app = Flask(__name__)

# Gmail setup
# Configure the Gmail user and password credentials via environment variables also provide your own gmail and password thet you get
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def generate_email_response(user_data, client_email):
    """
    Generate a professional email response using Google Gemini AI API.

    Args:
        user_data (dict): Dictionary containing client details.
        client_email (str): Email address of the client to whom the email will be sent.

    """
    # Configure the API key for Gemini
    genai.configure(api_key=os.getenv("GENERATIVE_AI_API_KEY"))  # API key from environment variables
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use Gemini's model

    # Prepare input content from user data
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

    # Construct the AI prompt to generate a professional email
    prompt = f"""
    You are a professional project manager responding to a client inquiry about a web development project. Below are the client details:
    {input_content}

    Based on this information, generate a clear and concise email response that:
    1. Acknowledges the client's inquiry.
    2. Summarizes their project requirements clearly (e.g., what pages and filters they need).
    3. Mentions their budget and politely invites them to schedule a call to discuss further and align expectations.
    4. Is professional, polite, and friendly.
    5. Sign off with a professional closing, including a signature.
    6. Includes only the signature: "Best regards, Jesna" or "Best regards, Jesna, Project Manager, XYZ Solutions".
    7. Ensure the email does not include placeholders like [Your Name], [Your Title], or [Your Contact Information].

    The email should be formatted as follows:
    - Salutation with the client’s full name.
    - A brief introduction and summary of their project.
    - A closing with your professional signature.
    """

    try:
        # Use the Gemini API to generate the email content
        response = model.generate_content(prompt)

        # Extract the generated email content
        generated_email = response.text.strip()

        # Signature
        signature = """
        Best regards,
        Jesna
        Project Manager
        XYZ Solutions
        """

        # Full message with signature
        full_message = f"{generated_email}\n\n{signature}"

        # Send the email
        send_email(client_email, full_message)

    except Exception as e:
        print(f"Error generating email response: {e}")

def send_email(client_email, message):
    """
    Send the generated email response to the client using Gmail SMTP.

    Args:
        client_email (str): Recipient email address.
        message (str): Email content to be sent.
    """
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=GMAIL_USER, password=GMAIL_PASSWORD)
        connection.sendmail(
            from_addr=GMAIL_USER,
            to_addrs=client_email,
            msg=f"Subject: Project Inquiry Response\n\n{message}".encode("utf-8")
        )

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Handle webhook calls from Google Apps Script or other sources.
    
    Expects JSON data containing client details.
    """
    data = request.get_json()  # Retrieve the data from the webhook

    if data:
        # Extract user data from the incoming JSON
        user_data = {
            "timestamp": data["timestamp"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "country": data["country"],
            "location": data["location"],
            "project_type": data["project_type"],
            "service_category": data["service_category"],
            "website": data["website"],
            "additional_info": data["additional_info"],
            "budget": data["budget"],
        }

        # Generate and send the email response
        generate_email_response(user_data, user_data["email"])
        return jsonify({"status": "success", "message": "Email sent!"})
    else:
        return jsonify({"status": "error", "message": "No data received!"}), 400

if __name__ == "__main__":
    # Start the Flask server
    app.run(debug=True)
