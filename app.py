import os
from flask import Flask, request, render_template
from openai import OpenAI

app = Flask(__name__)

# --- API CONFIG ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
else:
    print(f"Using API key: {api_key[:7]}...{api_key[-4:]}")  # Masked for safety

client = OpenAI(api_key=api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-guidance', methods=['POST'])
def get_guidance():
    try:
        skills = request.form.get('skills', '')
        strengths = request.form.get('strengths', '')
        interests = request.form.get('interests', '')

        prompt = (
            f"As a career guidance expert, suggest suitable career paths based on "
            f"the following details:\n"
            f"Skills: {skills}\n"
            f"Strengths: {strengths}\n"
            f"Interests: {interests}\n"
            f"Provide a concise, clear, and encouraging response."
        )

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4o" (fast) or "gpt-4" (slower, more detailed)
            messages=[
                {"role": "system", "content": "You are a helpful career coach."},
                {"role": "user", "content": prompt}
            ]
        )

        guidance = response.choices[0].message.content
        return render_template('result.html', response=guidance)

    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template(
            'result.html',
            response=f"An error occurred while generating guidance: {e}"
        )

if __name__ == '__main__':
    app.run(debug=True)
