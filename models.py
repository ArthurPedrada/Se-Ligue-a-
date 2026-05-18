from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Adicionamos UserMixin para compatibilidade com o Flask-Login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # nullable=False adicionado para garantir que dados essenciais sempre existam
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    events = db.relationship('Event', backref='user', lazy=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    # description pode continuar permitindo nulo caso o usuário não queira detalhar
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    # nullable=False garante que todo evento pertença obrigatoriamente a um usuário
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)