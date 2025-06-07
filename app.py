from flask import Flask
from extensions import db
from routes import blueprints
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)


    for bp in blueprints:
        app.register_blueprint(bp)

    from routes.main import register_error_handlers
    register_error_handlers(app)
    
    return app

app = create_app()