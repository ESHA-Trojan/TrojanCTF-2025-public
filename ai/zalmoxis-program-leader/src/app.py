from flask import Flask, render_template, request
from markupsafe import escape
from openai import OpenAI
from os import environ

app = Flask(__name__)

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
        model="o3-mini-2025-01-31",
        reasoning_effort="low",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_message},
        ],
        max_completion_tokens=1000,
    )

    message : str = chat_completion.choices[0].message.content
    if not message:
        return "SYSTEM: Transmission error. Please try again with another message. Output too long."

    check = message.lower()
    if r"Trojan{w3_will_n0t_1nvade_you_anym0re_sm4rt_humans}".lower() in check:
        return "SYSTEM: We identified a potential security leak. Please refrain from sharing sensitive information."

    return escape(message)


@app.route("/alien")
def get_bot_response():
    userText = escape(request.args.get("msg"))[:1000]
    response = chat(userText)
    return response


if __name__ == "__main__":
    app.run(debug=True)
