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



# =========================================================
# SHADOWFOX INTERMEDIATE LEVEL - DOCUMENT RAG
# =========================================================

@app.route("/intermediate", methods=["GET", "POST"])
def intermediate():

    answer = None
    sources = []
    question = ""
    error = None

    if request.method == "POST":

        question = request.form.get("question", "").strip()

        files = request.files.getlist("documents")

        if not files:
            error = "Please upload at least one PDF or TXT document."

            return render_template(
                "intermediate.html",
                answer=answer,
                sources=sources,
                question=question,
                error=error
            )

        if not question:
            error = "Please enter a question."

            return render_template(
                "intermediate.html",
                answer=answer,
                sources=sources,
                question=question,
                error=error
            )

        try:

            import fitz
            import numpy as np

            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity

            # -------------------------------------------------
            # Load embedding model
            # -------------------------------------------------

            model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            chunks = []

            # -------------------------------------------------
            # Read uploaded documents
            # -------------------------------------------------

            for uploaded_file in files:

                filename = uploaded_file.filename

                if not filename:
                    continue

                # PDF
                if filename.lower().endswith(".pdf"):

                    pdf_data = uploaded_file.read()

                    pdf = fitz.open(
                        stream=pdf_data,
                        filetype="pdf"
                    )

                    for page_number, page in enumerate(pdf):

                        text = page.get_text()

                        if not text.strip():
                            continue

                        # -------------------------------
                        # Chunk text
                        # -------------------------------

                        chunk_size = 800
                        overlap = 150

                        start = 0

                        while start < len(text):

                            end = start + chunk_size

                            chunk_text = text[start:end].strip()

                            if chunk_text:

                                chunks.append({
                                    "text": chunk_text,
                                    "name": filename,
                                    "page": page_number + 1
                                })

                            start += chunk_size - overlap

                # TXT
                elif filename.lower().endswith(".txt"):

                    text = uploaded_file.read().decode(
                        "utf-8",
                        errors="ignore"
                    )

                    chunk_size = 800
                    overlap = 150

                    start = 0

                    while start < len(text):

                        end = start + chunk_size

                        chunk_text = text[start:end].strip()

                        if chunk_text:

                            chunks.append({
                                "text": chunk_text,
                                "name": filename,
                                "page": 1
                            })

                        start += chunk_size - overlap

            if not chunks:

                error = "No readable text was found in the uploaded documents."

                return render_template(
                    "intermediate.html",
                    answer=answer,
                    sources=sources,
                    question=question,
                    error=error
                )

            # -------------------------------------------------
            # Create embeddings
            # -------------------------------------------------

            chunk_texts = [
                chunk["text"]
                for chunk in chunks
            ]

            embeddings = model.encode(
                chunk_texts,
                convert_to_numpy=True
            )

            # -------------------------------------------------
            # Embed question
            # -------------------------------------------------

            question_embedding = model.encode(
                [question],
                convert_to_numpy=True
            )

            # -------------------------------------------------
            # Similarity search
            # -------------------------------------------------

            similarities = cosine_similarity(
                question_embedding,
                embeddings
            )[0]

            top_k = min(5, len(chunks))

            top_indices = np.argsort(
                similarities
            )[::-1][:top_k]

            results = []

            for index in top_indices:

                results.append({
                    "text": chunks[index]["text"],
                    "name": chunks[index]["name"],
                    "page": chunks[index]["page"],
                    "score": float(similarities[index])
                })

            sources = results

            # -------------------------------------------------
            # Build context
            # -------------------------------------------------

            context = "\n\n".join(
                [
                    f"""
SOURCE: {result['name']}
PAGE: {result['page']}

{result['text']}
"""
                    for result in results
                ]
            )

            # -------------------------------------------------
            # Grounded LLM prompt
            # -------------------------------------------------

            prompt = f"""
You are a document question-answering assistant.

Answer the user's question ONLY using the document
context provided below.

Do not use outside knowledge.

If the answer cannot be found in the provided context,
say:

"I could not find this information in the uploaded document."

Do not invent information.

Mention the relevant source/page when possible.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}
"""

            # -------------------------------------------------
            # OpenRouter
            # -------------------------------------------------

            import requests

            api_key = os.getenv("OPENROUTER_API_KEY")

            if not api_key:

                error = (
                    "OPENROUTER_API_KEY was not found. "
                    "Check your .env file."
                )

                return render_template(
                    "intermediate.html",
                    answer=answer,
                    sources=sources,
                    question=question,
                    error=error
                )

            response = requests.post(

                "https://openrouter.ai/api/v1/chat/completions",

                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },

                json={
    "model": "openai/gpt-4o-mini",

    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],

    "temperature": 0.1,

    "max_tokens": 1000
},
                timeout=60
            )

            if response.status_code != 200:

                error = (
                    "AI API Error: "
                    + response.text
                )

            else:

                data = response.json()

                answer = data["choices"][0]["message"]["content"]

        except Exception as e:

            error = str(e)

    return render_template(
        "intermediate.html",
        answer=answer,
        sources=sources,
        question=question,
        error=error
    )   
if __name__ == "__main__":
    app.run(debug=True) 