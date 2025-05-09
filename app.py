from flask import Flask
from routes import blueprints
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True, port=8080)