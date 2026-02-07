from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
import google.generativeai as genai
from domain_registry import DOMAIN_REGISTRY
from schema_engine import build_structured_prompt

load_dotenv()

genai.configure(api_key=os.getenv("LLM_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)
app.secret_key = "structify-secret"


@app.route("/")
def home():
    return render_template("index.html", domains=DOMAIN_REGISTRY)


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json

        topic = data["topic"]
        domain = data["domain"]
        output_type = data["output_type"]
        level = data["level"]
        sections = data["sections"]  # list of edited section names

        prompt = build_structured_prompt(
            topic,
            domain,
            output_type,
            level,
            sections
        )

        response = model.generate_content(prompt)
        result = response.text

        session["last_output"] = result
        session["last_sections"] = sections

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})


@app.route("/refine", methods=["POST"])
def refine():
    try:
        data = request.json
        refinement = data["refinement"]

        previous_output = session.get("last_output")
        sections = session.get("last_sections")

        if not previous_output:
            return jsonify({"result": "No previous output found."})

        section_text = "\n".join(sections)

        refine_prompt = f"""
You are Structify refinement engine.

Previous Output:
{previous_output}

Refinement Instruction:
{refinement}

Maintain EXACT section names and order:
{section_text}

Do NOT return JSON.
"""

        response = model.generate_content(refine_prompt)
        result = response.text

        session["last_output"] = result

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"result": f"Refinement Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
