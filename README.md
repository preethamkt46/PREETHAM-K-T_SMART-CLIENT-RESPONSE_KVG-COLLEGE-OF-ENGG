SMART-CLIENT-RESPONSE

A Python-based application designed to provide intelligent client responses by leveraging OpenAI and Gemini APIs.

📜 Overview

SMART-CLIENT-RESPONSE is a powerful tool to enhance client interactions through AI-driven responses. It utilizes the OpenAI API or Gemini API for natural language processing and advanced generative capabilities.

## ✨ How It Works

1. **User Submission**:
   - A client submits a Google Form.

2. **Google Sheets**:
   - The data is added to a connected Google Sheet.

3. **App Script Trigger**:
   - Automatically sends the form data to the Flask app via the configured webhook.

4. **SMART-CLIENT-RESPONSE**:
   - Processes the data, generates a response using OpenAI/Gemini APIs, and sends an email back to client.

---


🛠️ Features

AI-Powered Client Responses: Uses OpenAI's API for intelligent and context-aware replies.
Email Integration: Sends responses via email using smtplib.
Multi-API Support: Combines the power of OpenAI or Gemini APIs for comprehensive solutions.

🛠️ Tech Stack

Backend Framework: Flask
APIs Used:# any one:
OpenAI API
Gemini API
Email Integration: smtplib

🚀 Getting Started
Prerequisites



# SMART-CLIENT-RESPONSE

SMART-CLIENT-RESPONSE is a Python application designed to deliver intelligent client responses by leveraging **OpenAI** or **Gemini** APIs. The application also integrates with **Google Sheets** to trigger responses via email upon form submissions.

---

📜 Overview

SMART-CLIENT-RESPONSE is a powerful tool to enhance client interactions through AI-driven responses. It utilizes the OpenAI API or Gemini API for natural language processing and advanced generative capabilities.

## 🛠️ Features
- AI-powered responses using OpenAI or Gemini APIs.
- Automatic email notifications triggered by Google Form submissions.
- Seamless integration with Google Sheets and Google Cloud APIs.

---

## 📋 Prerequisites

Before starting, ensure you have the following:

1. **API Keys**:
   - OpenAI API Key: Required to use OpenAI models.
   - Gemini API Key: For enhanced AI capabilities. Example configuration:
     ```python
     genai.configure(api_key="YOUR_API_KEY")
     model = genai.GenerativeModel("gemini-1.5-flash")
     ```

2. **Gmail Credentials**:
   - A Gmail account to send email responses. Example setup:
     ```python
     my_email = "EXAMPLE@gmail.com"  # Your Gmail address
     password = "abcd abcd abcd abcd"  # Your Gmail app-specific password
     ```

3. **Google Cloud Setup**:
   - Enable **Google Sheets API** in the Google Cloud Console.
   - Generate a **Service Account Key** (JSON format) and download it for use.

4. **Google Sheets Integration**:
   - Deploy the `main.py` script and add the URL of deployment to **App Script** in Google Sheets to automate response handling.

---

## 🚀 Installation and Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/PREETHAM-K-T_SMART-CLIENT-RESPONSE_KVG-COLLEGE-OF-ENGG.git
cd PREETHAM-K-T_SMART-CLIENT-RESPONSE_KVG-COLLEGE-OF-ENGG
```

### 2️⃣ Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Keys
Set up your API keys and email credentials in a `.env` file:
```env
OPENAI_API_KEY=your-openai-api-key
or
GEMINI_API_KEY=your-gemini-api-key
EMAIL_USER=example@gmail.com
EMAIL_PASS=abcd abcd abcd abcd
service accout.json
```

### 5️⃣ Set Up Google Sheets Integration
1. **Enable APIs**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **Google Sheets API**.
   - Download the **Service Account Key** as a JSON file and place it in your project directory.

2. **Deploy the App Script**:
   - Open Google Sheets > **Extensions** > **App Script**.
   - Replace the script with the following:
     ```javascript
     function onFormSubmit(e) {
         var data = e.values;

         var url = "https://your-flask-app-url";  // Replace with your Flask app's deployed URL
         var payload = {
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
             "budget": data[10]
         };

         var options = {
             "method": "post",
             "contentType": "application/json",
             "payload": JSON.stringify(payload)
         };

         UrlFetchApp.fetch(url, options);
     }

     function createTrigger() {
         ScriptApp.newTrigger("onFormSubmit")
             .forSpreadsheet(SpreadsheetApp.getActiveSpreadsheet())
             .onFormSubmit()
             .create();
     }
     ```
   - Deploy the script and set up triggers.

---

## 🖥️ Running the Application

1. Start the Flask server locally:
   ```bash
   python app.py
   ```
2. Deploy your Flask app to a hosting platform (e.g., AWS, Heroku, or Google Cloud) and update the webhook URL in the App Script.

3. Test the integration by submitting a Google Form response.

---


## 👤 Author
- **Preetham K T**  
---
