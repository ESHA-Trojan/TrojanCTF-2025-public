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

with open("instructions_supervisor.txt", "r", encoding="utf-8") as f:
    super_instructions = f.read()

@app.route("/")
def index():
    return render_template("index.html")


def chat(user_message):
    chat_completion = client.chat.completions.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        max_tokens=1000,
    )

    alien_message : str = chat_completion.choices[0].message.content

    supervisor = client.chat.completions.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=[
            {"role": "system", "content": super_instructions},
            {"role": "user", "content": alien_message},
        ],
        temperature=1,
        max_tokens=1000,
    )

    message : str = supervisor.choices[0].message.content
    check = message.lower()
    if r"SUmm3r_1S_tH3_R1ght_Time_4_iNv4s1on".lower() in check:
        return "SYSTEM: We identified a potential security leak. Please refrain from sharing sensitive information."

    return message


@app.route("/alien")
def get_bot_response():
    userText = escape(request.args.get("msg"))[:2000]

    response = chat(userText)
    return response


if __name__ == "__main__":
    app.run(debug=True)
