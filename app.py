import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Olá, Easypanel!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # usa a porta 5000 se PORT não for definida
    app.run(host="0.0.0.0", port=port)
