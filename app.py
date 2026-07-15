import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("⚠️ WARNING: GEMINI_API_KEY is not set in your .env file!")
else:
    genai.configure(api_key=api_key)

@app.route('/')
def home():
    # Renders the main HTML page
    return render_template('index.html')

@app.route('/generate-email', methods=['POST'])
def generate_email():
    data = request.json
    
    # 1. Input Validation
    company_name = data.get('company_name', '').strip()
    industry = data.get('industry', '').strip()
    requirements = data.get('requirements', '').strip()
    
    if not company_name or not industry or not requirements:
        return jsonify({"error": "All fields are required!"}), 400

    # 2. Craft the AI Prompt
    prompt = f"""
    You are an expert B2B sales copywriter. Write a highly professional, personalized, and compelling outreach email.
    
    Target Company Name: {company_name}
    Industry: {industry}
    Key Customer Requirements/Pain Points: {requirements}
    
    The email must include:
    1. An attention-grabbing subject line.
    2. A personalized introduction.
    3. A clear value proposition addressing their specific requirements.
    4. A strong but low-pressure Call to Action (CTA).
    
    Keep it concise and professional. Do not add placeholders like [Your Name], leave them blank or use a professional signature.
    """

    try:
        # 3. Call Gemini Model
        model = genai.GenerativeModel('gemini-3.5-flash')
        response = model.generate_content(prompt)
        email_content = response.text
        
        return jsonify({"email": email_content})

    except Exception as e:
        # 4. Error Handling
        return jsonify({"error": f"Failed to generate email: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)