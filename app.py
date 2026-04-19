import os
from google import genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- 1. SECURE BRAIN SETUP ---
# It looks for a "Secret" named GEMINI_API_KEY on the server.
# If it doesn't find it, it uses your key as a backup.
api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAn43LqV9GdQk66ITSO4iG4-26vrLll-Wc")
client = genai.Client(api_key=api_key)

def get_bot_response(user_input):
    try:
        # Using the absolute latest 2026 stable model
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=user_input,
            config={'system_instruction': 'You are a witty AI assistant for a dark-mode web app.'}
        )
        return response.text
    except Exception as e:
        print(f"Error: {e}") 
        return "Brain Error: I'm having trouble connecting right now."

# --- 2. ROUTES ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot():
    # Adding a check to make sure message isn't empty
    user_text = request.form.get("msg", "")
    if not user_text:
        return jsonify({"reply": "I didn't hear anything! Try typing a message."})
        
    response = get_bot_response(user_text)
    return jsonify({"reply": response})

# --- 3. SERVER LAUNCH ---
if __name__ == "__main__":
    # When live on the web, servers use a 'PORT' variable. 
    # This line ensures your app works locally and in the cloud.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)