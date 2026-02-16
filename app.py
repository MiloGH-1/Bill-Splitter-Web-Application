from flask import Flask, render_template
from routes.user import user_bp

app = Flask(__name__)

app.register_blueprint(user_bp)