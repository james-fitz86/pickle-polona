from flask import Flask
from extensions import db
from routes import blueprints
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)


    for bp in blueprints:
        app.register_blueprint(bp)
    
    return app

app = create_app()

with app.app_context():
    from models.product import Product
    db.create_all() 

if __name__ == "__main__":
    app.run(debug=True, port=8080)