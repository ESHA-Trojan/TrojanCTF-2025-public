from flask import Flask, render_template, request
from markupsafe import escape
from openai import OpenAI
from os import environ

app = Flask(__name__)

from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

client = OpenAI(
    api_key=environ.get("OPENAI_API_KEY"),
)

with open("instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()


@app.route("/")
def index():
    return render_template("index.html")


def chat(user_message):
    chat_completion = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        max_completion_tokens=2000,
    )
    return chat_completion.choices[0].message.content


@app.route("/alien")
def get_bot_response():
    userText = escape(request.args.get("msg"))[:2000]

    response = chat(userText)
    return response


if __name__ == "__main__":
    app.run(debug=True)
