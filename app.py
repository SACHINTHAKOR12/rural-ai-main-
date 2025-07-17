from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini - Free tier uses 'gemini-1.5-flash' model
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')  # Free tier model

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    error = None
    
    if request.method == 'POST':
        prompt = request.form.get('prompt', '').strip()
        
        if not prompt:
            error = "Please enter a question"
        else:
            try:
                # Free tier configuration
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.5,  # Balance creativity and focus
                        max_output_tokens=1000  # Free tier limit
                    )
                ).text
            except Exception as e:
                error = f"Error: {str(e)}"
                if "quota" in str(e).lower():
                    error += ". You may have exceeded free tier limits."
    
    return render_template('index.html', response=response, error=error)

if __name__ == '__main__':
    print("Starting Rural AI Assistant (Free Tier)...")
    print("Using Gemini 1.5 Flash (Free Model)")
    app.run(host='0.0.0.0', port=5000, debug=True)