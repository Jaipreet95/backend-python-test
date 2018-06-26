from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    session
    )
from alayatodo import app,db
from .models import Users, Todo


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Users.query.filter_by(username=username, password=password)
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todo.query.get(int(id))
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    todos = Todo.query.all()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    if request.form.get('description'):
        u = Users.query.get(int(session['user']['id']))
        t = Todo(description=request.form.get('description'),users=u)
        db.session.add(t)
        db.session.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_is_completed(id):
    if not session.get('logged_in'):
        return redirect('/login')
    t = Todo.query.get(int(id))
    t.is_completed = True
    db.session.add(t)
    db.session.commit()

    return redirect('/todo')

@app.route('/todo/<id>/json', methods=['GET'])
@app.route('/todo/<id>/json/', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.get(int(id))
    t = {
        'id': todo.id,
        'description': todo.description,
        'is_completed': todo.is_completed,
        'user_id': todo.user_id
    }
    return jsonify(t)

@app.route('/todo/delete/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    db.session.delete(Todo.query.get(int(id)))
    db.session.commit()
    return redirect('/todo')
