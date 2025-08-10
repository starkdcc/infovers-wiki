import openai
import os
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

topics = [
    "History of the Internet",
    "Quantum Computing",
    "Ancient Egypt",
    "Space Exploration",
    "Artificial Intelligence",
    "The Great Wall of China",
    "Climate Change",
    "Leonardo da Vinci",
    "Blockchain Technology",
    "Black Holes"
]

def generate_article(topic):
    prompt = f"""
    Write a detailed Wikipedia-style article about '{topic}'.
    Include Introduction, History, Key Facts, and References.
    Around 800 words, neutral tone.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message["content"]

def save_article(topic, content):
    filename = f"articles/{topic.lower().replace(' ', '-')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"<h1>{topic}</h1>\n<p>{content}</p>")
    return filename

def update_index():
    articles = sorted(os.listdir("articles"))
    links = [f'<li><a href="articles/{a}">{a.replace("-", " ").replace(".html", "").title()}</a></li>' for a in articles]
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>InfoVerse AI</title>
      <link rel="stylesheet" href="styles.css">
    </head>
    <body>
      <h1>InfoVerse AI</h1>
      <p>Your AI-powered encyclopedia.</p>
      <ul>
        {''.join(links)}
      </ul>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    os.makedirs("articles", exist_ok=True)
    topic = random.choice(topics)
    text = generate_article(topic)
    save_article(topic, text)
    update_index()
