"""Todo_List widget.

This script allows to create a simple todo list widget. User has to create an
account to access to widget. He can then add task main tasks and subtasks. When
subtask is done, user can delete it, or just mark it as "done". In case of
error, he can of course edit the subtask previously created.

User also has the possibility to share his task with another user by enter his
name in text area meant for that purpose. When task is shared, all actions,
additions of subtasks, deletions will be propagated at all user.
"""

__author__ = ("Clément Daroit")
__contact__ = ("ceedar.lab@gmail.com")
__version__ = "1.0"
__date__ = "2020-11-09"

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Joining table between User and Task
assignee = db.Table(
    'assignee',
    db.Column('id_user', db.Integer, db.ForeignKey('user.id_user')),
    db.Column('id_task', db.Integer, db.ForeignKey('task.id_task'))
)


class User(db.Model):
    """Table of users.

    Many-to-many relationship with Task.
    """

    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    tasks = db.relationship('Task', secondary=assignee, back_populates='users')

    def __repr__(self):
        """Representation of table User."""
        return '<User %r>' % self.name


class Task(db.Model):
    """Table of tasks.

    Many-to-many relationship with User.
    One-to-many relationship with SubTask.
    """

    id_task = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, unique=True)
    creator = db.Column(
        db.Integer, db.ForeignKey('user.id_user'),
        nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', secondary=assignee, back_populates='tasks')

    def __repr__(self):
        """Representation of table Task."""
        return '<Task %r>' % self.title


class SubTask(db.Model):
    """Table of subtasks.

    Many-to-one relationship with Task.
    """

    id_subtask = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, default=1, nullable=False)
    id_task = db.Column(
        db.Integer, db.ForeignKey('task.id_task'),
        nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Representation of table SubTask."""
        return '<Subtask %r>' % self.title


# Global
id_task = 0


@app.route('/', methods=['POST', 'GET'])
def widget_functionalities():
    """Widget functionalities.

    Check the request sent by todo list application.
    Allows to create, delete, edit tasks and subtasks.
    Allows to share a task with another user.
    """
    id_user = 1
    global id_task
    tasks = Task.query.join(Task.users).filter(User.id_user == id_user).all()
    subTasks = SubTask.query.filter_by(id_task=id_task).all()

    if request.method == 'POST':
        # Shows list of created tasks
        if 'taskList' in request.form:
            id_task = request.form['taskList']
            subTasks = SubTask.query.filter_by(id_task=id_task).all()
            task = Task.query.get(id_task)
            return render_template(
                'index.html', task=task, subTasks=subTasks, tasks=tasks)
        # Allows to create new task
        elif 'add_task' in request.form:
            try:
                task_content = request.form['add_task']
                if task_content != "":
                    new_task = Task(title=task_content, creator=id_user)
                    user = User.query.get(id_user)
                    new_task.users.append(user)
                    db.session.add(new_task)
                    db.session.commit()
                    task = Task.query.order_by(
                        Task.date_created.desc()).first()
                    id_task = task.id_task
                    tasks = Task.query.filter_by(creator=id_user).order_by(
                        Task.date_created).all()
                    return render_template(
                        'index.html', task=task, tasks=tasks)
                else:
                    task = Task.query.get(id_task)
                    subTasks = SubTask.query.filter_by(id_task=id_task).all()
                    tasks = Task.query.filter_by(creator=id_user).order_by(
                        Task.date_created).all()
                    errorMessage = 'Veuiller entrer un titre'
                    return render_template(
                        'index.html',
                        task=task, subTasks=subTasks, tasks=tasks,
                        errorMessage=errorMessage)
            # In case of task already exists
            except Exception:
                db.session.rollback()
                task = Task.query.get(id_task)
                subTasks = SubTask.query.filter_by(id_task=id_task).all()
                tasks = Task.query.filter_by(creator=id_user).order_by(
                    Task.date_created).all()
                errorMessage = 'Cette tache existe déjà'
                return render_template(
                    'index.html',
                    task=task, subTasks=subTasks, tasks=tasks,
                    errorMessage=errorMessage)
        # Allows to delete task
        elif 'remove_task' in request.form:
            Task.query.filter_by(id_task=id_task).delete()
            SubTask.query.filter_by(id_task=id_task).delete()
            db.session.commit()
            id_task = 0
            return redirect('/')
        # Allows to create new subtask
        elif 'add_subTask' in request.form:
            subTask_content = request.form['add_subTask']
            new_subTask = SubTask(title=subTask_content, id_task=id_task)
            db.session.add(new_subTask)
            db.session.commit()
            task = Task.query.get(id_task)
            subTasks = SubTask.query.filter_by(id_task=id_task).all()
            return render_template(
                'index.html', task=task, subTasks=subTasks, tasks=tasks)
        # Allows to delete subtask
        elif 'remove_subTask' in request.form:
            id_subTask = request.form['id_subTask']
            SubTask.query.filter_by(id_subtask=id_subTask).delete()
            db.session.commit()
            task = Task.query.get(id_task)
            subTasks = SubTask.query.filter_by(id_task=id_task).all()
            return render_template(
                'index.html', task=task, subTasks=subTasks, tasks=tasks)
        # Allows to edit subtask
        elif 'edit_subTask' in request.form:
            subTask_content = request.form['edit_subTask']
            id_subTask = request.form['id_subTask']
            subTask_state = request.form['subTask_state']
            SubTask.query.filter_by(id_subtask=id_subTask).update(
                {SubTask.title: subTask_content})
            SubTask.query.filter_by(id_subtask=id_subTask).update(
                {SubTask.status: subTask_state})
            db.session.commit()
            task = Task.query.get(id_task)
            subTasks = SubTask.query.filter_by(id_task=id_task).all()
            return render_template(
                'index.html', task=task, subTasks=subTasks, tasks=tasks)
        # Allows to share a task with another user
        elif 'add_assignee' in request.form:
            try:
                new_assignee = request.form['add_assignee']
                new_assignee = User.query.filter_by(name=new_assignee).all()
                new_assignee = new_assignee[0]
                task = Task.query.get(id_task)
                task.users.append(new_assignee)
                db.session.add(task)
                db.session.commit()
                subTasks = SubTask.query.filter_by(id_task=id_task).all()
                errorMessage = 'utilisateur ajouté'
                return render_template(
                    'index.html', task=task, subTasks=subTasks, tasks=tasks,
                    errorMessage=errorMessage)
            # If user doesn't exist
            except Exception:
                db.session.rollback()
                task = Task.query.get(id_task)
                subTasks = SubTask.query.filter_by(id_task=id_task).all()
                tasks = Task.query.filter_by(creator=id_user).order_by(
                    Task.date_created).all()
                errorMessage = 'utilisateur inexistant'
                return render_template(
                    'index.html', task=task, subTasks=subTasks, tasks=tasks,
                    errorMessage=errorMessage)
    else:
        task = Task.query.get(id_task)
        return render_template(
            'index.html', task=task, subTasks=subTasks, tasks=tasks)
