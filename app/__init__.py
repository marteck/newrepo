from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b30edca0886e00babec771d023155e'
from app import routes



