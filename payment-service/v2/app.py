from flask import Flask, request
import time

app = Flask(__name__)

@app.route("/pay", methods=["POST"])
def pay():
    print("V2 (shadow) recebeu request real")
    print("Payload:", request.json)

    time.sleep(0.5)

    return {
        "version": "v2",
        "message": "Nova regra de pagamento"
    }, 200

@app.route("/health")
def health():
    return "ok", 200

app.run(host="0.0.0.0", port=8080)

