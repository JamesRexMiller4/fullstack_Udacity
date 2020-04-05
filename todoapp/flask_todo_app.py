from flask import Flask
from flask_sqlalchemy import sqlalchemy

app = Flask(__name__)
app.congif['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost:5432'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
  render_template('index.html', data=[{
    {
      'description': 'Todo 1'
    }, 
    {
      'description': 'Todo 2'
    }, 
    {
      'description': 'Todo 3'
    }
  }])