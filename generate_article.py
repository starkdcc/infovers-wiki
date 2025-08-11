import os
import requests
from openai import OpenAI
from datetime import datetime

# Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# --- Step 1: Generate article text ---
def generate_article(topic):
    prompt = f"Write an informative 500-word Wikipedia-style article about {topic}."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful and knowledgeable writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# --- Step 2: Get Unsplash image ---
def get_unsplash_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    r = requests.get(url)
    data = r.json()
    return data["urls"]["regular"], data["user"]["name"], data["links"]["html"]

# --- Step 3: Save to HTML file ---
def save_article(topic, text, image_url, photographer, photographer_url):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"articles/{today}.html"

    html_content = f"""
    <html>
    <head>
        <title>{topic} - InfoVerse Wiki</title>
        <link rel="stylesheet" href="../styles.css">
    </head>
    <body>
        <h1>{topic}</h1>
        <img src="{image_url}" alt="{topic}" style="max-width:100%;">
        <p><small>Photo by <a href="{photographer_url}" target="_blank">{photographer}</a> on Unsplash</small></p>
        <article>{text.replace('\n', '<br>')}</article>
    </body>
    </html>
    """

    os.makedirs("articles", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Article saved to {filename}")

# --- Main ---
if __name__ == "__main__":
    topic = "Latest AI News"
    article_text = generate_article(topic)
    image_url, photographer, photographer_url = get_unsplash_image("artificial intelligence")
    save_article(topic, article_text, image_url, photographer, photographer_url)
