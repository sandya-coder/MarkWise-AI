# MarkWise AI 🎓

MarkWise AI is an AI-powered student assistant that evaluates written exam answers and helps students improve them.

## Problem

Students often write answers without knowing:
- How many marks their answer may receive
- Which important points they missed
- What mistakes they made
- How to improve their answer for better marks

## Solution

MarkWise AI analyzes a student's answer using an LLM and provides structured academic feedback.

The student enters:
- Subject
- Exam question
- Maximum marks
- Their answer

The application then provides:
- Estimated score
- Correct points
- Missing points
- Mistakes
- Suggestions for improvement
- Improved examination-ready answer
- Key points to remember
- Tips to score full marks

## Features

- 🤖 AI-powered answer evaluation
- 📊 Estimated marks
- ✅ Correct point identification
- ❌ Missing point detection
- ⚠️ Mistake identification
- 💡 Personalized suggestions
- ✍️ Improved answer generation
- 🧠 Revision key points
- 🏆 Full-mark scoring tips
- 📋 Copy improved answer
- ⚠️ Input validation
- 📱 Mobile-friendly interface

## How It Works

1. Student enters the subject.
2. Student enters the exam question.
3. Student enters the maximum marks.
4. Student writes their answer.
5. MarkWise AI sends the information to an LLM.
6. The AI evaluates the answer according to the question and marks.
7. The feedback is displayed on the webpage.

## Technology Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- OpenRouter API
- Requests
- python-dotenv
- Gunicorn

## Project Structure

```text
MarkWise-AI/
│
├── templates/
│   └── index.html
│
├── app.py
├── .env
├── .gitignore
├── Procfile
├── README.md
└── requirements.txt