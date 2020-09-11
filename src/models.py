from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    tasks = db.relationship("Task", backref="usuario")

    def __init__(self, name):
        self.name = name

    @classmethod
    def register(cls, name):
        new_user = cls(
            name
        )
        return new_user

    def serialize(self):
        tasks_list = self.tasks
        list_tasks = []
        for task in tasks_list:
            list_tasks.append(task.label)
        return{
            "id": self.id,
            "name": self.name,
            "tasks": list_tasks
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    def __init__(self, label, done, usuario_id):
        self.label = label
        self.done = done
        self.usuario_id = usuario_id

    @classmethod
    def register(cls, label, done, usuario_id):
        new_task = cls(
            label,
            done,
            usuario_id
        )
        return new_task

    def serialize(self):
        return{
            "id": self.id,
            "label": self.label,
            "done": self.done,
            "usuario_id": self.usuario_id
        }