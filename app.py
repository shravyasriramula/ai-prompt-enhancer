from flask import Flask, render_template, request, jsonify
import requests
from config import GROK_API_KEY

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.get_json()

        user_prompt = data.get("prompt")
        style = data.get("style")

        prompt = f"""
You are an expert AI Prompt Engineer.

Object:
{user_prompt}

Style:
{style}

Create a highly detailed image generation prompt.

Include:

- Subject details
- Colors
- Materials
- Environment
- Lighting
- Atmosphere
- Mood
- Camera angle
- Lens type
- Composition
- Ultra quality keywords

Length:
100-150 words.

Return only the prompt.
"""

        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={
                "model": "llama-3.3-70b-specdec",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
        )

        response_data = response.json()
        
        if "choices" not in response_data:
            print(f"Unexpected response: {response_data}")
            return jsonify({
                "success": False,
                "error": f"API Error: {response_data}"
            })

        result = response_data["choices"][0]["message"]["content"]

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)