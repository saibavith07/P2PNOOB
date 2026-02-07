from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found in .env")

genai.configure(api_key=API_KEY)

# ✅ Use working model from your list
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json

        topic = data.get("topic", "")
        domain = data.get("domain", "Project Blueprint")
        level = data.get("level", "Medium")
        constraints = data.get("constraints", "")

        prompt = build_prompt(topic, domain, level, constraints)

        response = model.generate_content(prompt)

        return jsonify({"result": response.text})

    except Exception as e:
        return jsonify({"result": f"Server Error: {str(e)}"})


def build_prompt(topic, domain, level, constraints):

    return f"""
You are Structify — a structured execution engine.

Your job is to generate a structured {domain}.

Follow this section order strictly:

1. Problem Statement
2. Target Users
3. Key Pain Points
4. Proposed Solution
5. Key Features
6. Technology Stack
7. Feasibility
8. Future Scope

Topic: {topic}

Complexity Level: {level}
Interpret level as:
- Basic → Simple explanation
- Medium → Moderate clarity
- High → Technical depth
- Advanced → Architecture-level execution detail

User Constraints:
{constraints if constraints else "None"}

Rules:
- Maintain strict section order.
- Apply constraints logically across sections.
- Do not skip sections.
- Keep professional tone.
"""

if __name__ == "__main__":
    app.run(debug=True)
