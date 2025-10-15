from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def bridge():
    github_token = os.getenv("ACCESS_TOKEN")
    if not github_token:
        return jsonify({"error": "Missing ACCESS_TOKEN"}), 500

    github_url = "https://api.github.com/repos/alirezalu1404/hamahang-callback/dispatches"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_token}",
        "Content-Type": "application/json"
    }
    payload = {"event_type": "kenar_message_created"}
    r = requests.post(github_url, json=payload, headers=headers)
    return jsonify({
        "status": "ok" if r.status_code in [200, 204] else "fail",
        "github_status": r.status_code,
        "response": r.text
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
