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
__version__ = "1.1"
__date__ = "2020-11-14"

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
    title = db.Column(db.String(30), db.CheckConstraint(
        'length(title) <= 20'), nullable=False, unique=True)
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
    title = db.Column(db.String(100), db.CheckConstraint(
        'length(title) <= 25'), nullable=False)
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
page_num = 1


@app.route('/', methods=['POST', 'GET'])
def widget_functionalities():
    """Widget functionalities.

    Check the request sent by todo list application.
    Allows to create, delete, edit tasks and subtasks.
    Allows to share a task with another user.
    """
    id_user = 1
    global id_task
    global page_num
    tasks = Task.query.join(Task.users).filter(User.id_user == id_user).all()

    def show(id, num):
        global id_task
        global page_num
        id_task = id
        page_num = num
        subTasks = SubTask.query.filter_by(id_task=id_task).paginate(
            page=page_num, per_page=7, error_out=False)
        task = Task.query.get(id_task)
        return task, subTasks

    if request.method == 'POST':
        # Shows selected task
        if 'taskList' in request.form:
            show = show(int(request.form['taskList']), 1)
            return render_template(
                'index.html', task=show[0], subTasks=show[1], tasks=tasks)
        # Shows previous page of subtasks
        elif 'prevPage' in request.form:
            show = show(id_task, int(request.form['prevPage']))
            return render_template(
                'index.html', task=show[0], subTasks=show[1], tasks=tasks)
        # Shows next page of subtasks
        elif 'nextPage' in request.form:
            show = show(id_task, int(request.form['nextPage']))
            return render_template(
                'index.html', task=show[0], subTasks=show[1], tasks=tasks)
        # Allows to create new task
        elif 'add_task' in request.form:
            try:
                task_content = request.form['add_task']
                if task_content == "" or len(task_content) > 20:
                    show = show(id_task, page_num)
                    tasks = Task.query.filter_by(creator=id_user).order_by(
                        Task.date_created).all()
                    errorMessage = "Veuillez entrer un titre valide"
                    return render_template(
                        'index.html',
                        task=show[0], subTasks=show[1], tasks=tasks,
                        errorMessage=errorMessage)
                else:
                    new_task = Task(title=task_content, creator=id_user)
                    user = User.query.get(id_user)
                    new_task.users.append(user)
                    db.session.add(new_task)
                    db.session.commit()
                    task = Task.query.order_by(
                        Task.date_created.desc()).first()
                    show = show(task.id_task, 1)
                    tasks = Task.query.filter_by(creator=id_user).order_by(
                        Task.date_created).all()
                    return render_template(
                        'index.html', task=show[0], subTasks=show[1],
                        tasks=tasks)
            # In case of task already exists
            except Exception:
                db.session.rollback()
                show = show(id_task, page_num)
                tasks = Task.query.filter_by(creator=id_user).order_by(
                    Task.date_created).all()
                errorMessage = "Cette tâche existe déjà"
                return render_template(
                    'index.html',
                    task=show[0], subTasks=show[1], tasks=tasks,
                    errorMessage=errorMessage)
        # Allows to delete task
        elif 'remove_task' in request.form:
            SubTask.query.filter_by(id_task=id_task).delete()
            task = Task.query.get(id_task)
            task.users.clear()
            db.session.delete(task)
            db.session.commit()
            return redirect('/')
        # Allows to create new subtask
        elif 'add_subTask' in request.form:
            subTask_content = request.form['add_subTask']
            if subTask_content == "" or len(subTask_content) > 25:
                show = show(id_task, page_num)
                tasks = Task.query.filter_by(creator=id_user).order_by(
                    Task.date_created).all()
                errorMessage = "Veuillez entrer un titre valide"
                return render_template(
                    'index.html',
                    task=show[0], subTasks=show[1], tasks=tasks,
                    errorMessage=errorMessage)
            else:
                new_subTask = SubTask(title=subTask_content, id_task=id_task)
                db.session.add(new_subTask)
                db.session.commit()
                last_page = SubTask.query.filter_by(id_task=id_task).paginate(
                    page=page_num, per_page=7, error_out=False)
                show = show(id_task, last_page.pages)
                return render_template(
                    'index.html', task=show[0], subTasks=show[1], tasks=tasks)
        # Allows to delete subtask
        elif 'remove_subTask' in request.form:
            id_subTask = request.form['id_subTask']
            SubTask.query.filter_by(id_subtask=id_subTask).delete()
            db.session.commit()
            last_page = SubTask.query.filter_by(id_task=id_task).paginate(
                page=page_num, per_page=7, error_out=False)
            show = show(id_task, last_page.pages)
            return render_template(
                'index.html', task=show[0], subTasks=show[1], tasks=tasks)
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
            show = show(id_task, page_num)
            return render_template(
                'index.html', task=show[0], subTasks=show[1], tasks=tasks)
        # Allows to share a task with another user
        elif 'add_assignee' in request.form:
            try:
                new_assignee = request.form['add_assignee']
                new_assignee = User.query.filter_by(name=new_assignee).all()
                new_assignee = new_assignee[0]
                show = show(id_task, page_num)
                show[0].users.append(new_assignee)
                db.session.add(show[0])
                db.session.commit()
                errorMessage = "Utilisateur ajouté"
                return render_template(
                    'index.html', task=show[0], subTasks=show[1], tasks=tasks,
                    errorMessage=errorMessage)
            # If user doesn't exist
            except Exception:
                db.session.rollback()
                show = show(id_task, page_num)
                errorMessage = "Utilisateur inexistant"
                return render_template(
                    'index.html', task=show[0], subTasks=show[1], tasks=tasks,
                    errorMessage=errorMessage)
    else:
        show = show(0, 1)
        return render_template(
            'index.html', task=show[0], subTasks=show[1], tasks=tasks)
