from flask import Flask
from app.routes import upload_bp, movies_bp
from mongoengine import connect

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Initialize MongoEngine
    connect('movies', alias="movies")


    # Register blueprints (API routes)
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(movies_bp, url_prefix='/api/movies')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)