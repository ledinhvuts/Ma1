import os
import json

import openai
from flask import Flask, render_template, request, send_from_directory
from serpapi import GoogleSearch
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
serp_api_key = os.getenv("SERP_API_KEY")

headers = {
    'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63"
}

@app.route("/chat", methods=["POST"])
def chat():
    question = request.form.get("q")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(question),
        temperature=0.2,
        max_tokens=250,
        n=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["User:", "Sally:"]
    )
    print(response)
    return {
        'question': question,
        'answer': response
    }

@app.route("/googlesearch", methods=["POST"])
def search():
    question = request.form.get("q")
    return {
        'question': question,
        'answer': get_knowledge_graph(question)
    }

@app.route("/<path:file_path>")
def files(file_path):
    return send_from_directory('static', file_path)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def get_knowledge_graph(text):
    params = {
        "api_key": serp_api_key,
        "engine": "google",
        "q": text,
        "hl": "en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return json.dumps(results.get('answer_box', ""))


def generate_prompt(phrase):
    return """{}
Sally:""".format(
        phrase.capitalize()
    )
