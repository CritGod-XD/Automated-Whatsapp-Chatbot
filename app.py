from flask import Flask, request, jsonify
from agent import get_reply

app = Flask(__name__)

@app.route("/chat_api", methods=["POST"])
def chat_api():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Invalid request"}), 400

        user_msg = data["message"]
        reply = get_reply(user_msg)
        return jsonify({"reply": reply})

    except Exception as e:
        print(" API error:", e)
        return jsonify({"reply": "Something went wrong, try again."}), 500


if __name__ == "__main__":
    app.run(debug=False, threaded=True)
