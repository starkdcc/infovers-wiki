import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

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

if __name__ == "__main__":
    os.makedirs("articles", exist_ok=True)
    topic = "Alan Turing"
    text = generate_article(topic)
    save_article(topic, text)
