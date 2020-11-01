from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.name

class Task(db.Model):
    id_task = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    subtasks = db.relationship('SubTask', backref='task', lazy=True)

    def __repr__(self):
        return '<Task %r>' % self.title

class SubTask(db.Model):
    id_subtask = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  
    id_task = db.Column(db.Integer, db.ForeignKey('task.id_task'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Subtask %r>' % self.title

assignee = db.Table('assignee',
    db.Column('id_user', db.Integer, db.ForeignKey('user.id_user')),
    db.Column('id_subtask', db.Integer, db.ForeignKey('sub_task.id_subtask'))
)



@app.route('/', methods=['POST', 'GET'])
def add_task():
    session_user = 1  
    session_task = 0
    tasks = Task.query.filter_by(creator=session_user).order_by(Task.date_created).all() 
    task = Task.query.filter_by(id_task=session_task).all()
     
    if request.method == 'POST':
        # Selection de la tache à afficher
        if 'taskList' in request.form:
            session_task = request.form['taskList']
            subTasks = SubTask.query.filter_by(id_task=session_task).all()
            task = Task.query.get(session_task)
            return render_template('test.html', task=task, subTasks=subTasks, tasks=tasks, session_task=session_task)
        # Ajout d'une tache
        elif 'add_task' in request.form:
            task_content = request.form['add_task']
            new_task = Task(title=task_content, creator=session_user)
            db.session.add(new_task)
            db.session.commit()
            task = Task.query.order_by(Task.date_created.desc()).first()
            session_task = task.id_task
            tasks = Task.query.filter_by(creator=session_user).order_by(Task.date_created).all()
            return render_template('test.html', tasks=tasks, session_task=session_task)
        # Suppression d'une tache
        elif 'remove_task' in request.form: 
            session_task = request.form['session_task']        
            Task.query.filter_by(id_task=session_task).delete()
            SubTask.query.filter_by(id_task=session_task).delete()
            db.session.commit()
            return redirect('/')
        else:
            str = 'nothing'
            return render_template('test.html', str=str)

    else:
        return render_template('test.html', task=task, tasks=tasks, session_task=session_task)


#         task_content = request.form['task_content']
#         new_task = Task(title=task_content, creator=1)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Il y a un soucis'
#     else:
#         tasks = Task.query.order_by(Task.date_created).all()
#         return render_template('test.html', tasks=tasks)

# def add_subTask():
#     if request.method == 'POST':
#         subTask_content = request.form['subtask_content']
#         new_subTask = SubTask(title=subTask_content, id_task=1)

#         try:
#             db.session.add(new_subTask)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Il y a un soucis'
#     else:
#         subTasks = SubTask.query.filter(id_task=1).all()
#         return render_template('test.html', subTasks=subTasks)
