from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TodoList(db.Model):
  __tablename__ = 'todo_lists'
  id = db.Column(db.Integer, primary_key=True)
  list_name = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todo', backref='list', lazy=True)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean(), nullable=False, default=False)
  todo_list_id = db.Column(db.Integer, db.ForeignKey('todo_lists.id'), nullable=False)

# def __repr__(self):
#     return f'<Todo {self.id} {self.description}>'


@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description_value = request.get_json()['description']
    todo = Todo(description=description_value, completed=False)

    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except: 
    error = True
    db.session.rollback()
    print(sys.exc_info())
    
  finally:
    db.session.close()
  if error: 
    abort(400)
  else:
    return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed(todo_id):
  try:
    completed_value = request.get_json()['completed']
    todo = Todo.query.get(todo_id)
    todo.completed = completed_value
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))
    
@app.route('/delete/<todo_id>', methods=['DELETE'])
def remove_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })

@app.route('/lists/<todo_list_id>')
def get_list_todos(todo_list_id):
  return render_template('index.html', 
  lists=TodoList.query.all(),
  active_list=TodoList.query.get(todo_list_id),
  todos=Todo.query.filter_by(todo_list_id=todo_list_id).order_by('id').all())

@app.route('/')
def index():
  return redirect(url_for('get_list_todos', todo_list_id=1))


if __name__ == '__main__':
  app.run(debug=True)