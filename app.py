from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/evaluate", methods=["POST"])
def evaluate():

    data = request.get_json()

    subject = data.get("subject", "").strip()
    question = data.get("question", "").strip()
    marks = data.get("marks", "").strip()
    answer = data.get("answer", "").strip()

    if not subject or not question or not marks or not answer:
        return jsonify({
            "error": "Please fill in all fields."
        }), 400

    prompt = f"""
You are MarkWise AI, an academic answer evaluator.

Evaluate the student's answer fairly based on the
question and maximum marks.

Subject:
{subject}

Question:
{question}

Maximum Marks:
{marks}

Student's Answer:
{answer}

Give the evaluation in this format:


Return the evaluation using exactly these headings:

SCORE:
Give the estimated score out of {marks}.

CORRECT POINTS:
List 2 to 5 points the student answered correctly.
If none, say "No major correct points identified."

MISSING POINTS:
List the important points needed for a higher score.

MISTAKES:
List factual or conceptual mistakes.
If there are none, say "No major mistakes."

SUGGESTIONS:
Give 2 to 4 specific ways to improve the answer.

IMPROVED ANSWER:
Write a clear, examination-ready answer suitable for {marks} marks.

KEY POINTS TO REMEMBER:
Give exactly 3 to 5 short revision points.

HOW TO SCORE FULL MARKS:
Give 2 or 3 practical tips specifically for this question.

Keep the response concise, student-friendly, and easy to read.
Do not use Markdown symbols such as **, ##, or bullet symbols.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:

            print(response.text)

            return jsonify({
                "error": "AI service failed. Please try again."
            }), 500

        result = response.json()

        ai_answer = result["choices"][0]["message"]["content"]

        return jsonify({
            "result": ai_answer
        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": "Unable to connect to the AI service."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)