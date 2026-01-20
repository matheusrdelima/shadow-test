from flask import Flask, request
import time

app = Flask(__name__)

@app.route("/pay", methods=["POST"])
def pay():
    print("V1 - pagamento real")
    time.sleep(0.2)
    return {
        "version": "v1",
        "message": "Pagamento processado com sucesso"
    }, 200

@app.route("/health")
def health():
    return "ok", 200

app.run(host="0.0.0.0", port=8080)

