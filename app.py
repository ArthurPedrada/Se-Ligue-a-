from flask import Flask, render_template, request, redirect, url_for
from models import db, Event, User
from config import Config
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "segredo"

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# carregar usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password'])
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/')
@login_required
def agenda():
    events = Event.query.filter_by(user_id=current_user.id)\
                        .order_by(Event.date, Event.time).all()

    hoje = datetime.today().date()

    return render_template('agenda.html', events=events, hoje=hoje)


@app.route('/create', methods=['POST'])
@login_required
def create():
    date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    time = datetime.strptime(request.form['time'], '%H:%M').time()

    event = Event(
        title=request.form['title'],
        description=request.form['description'],
        date=date,
        time=time,
        user_id=current_user.id
    )

    db.session.add(event)
    db.session.commit()

    return redirect('/')


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    event = Event.query.get_or_404(id)

    if event.user_id == current_user.id:
        db.session.delete(event)
        db.session.commit()

    return redirect('/')

# 🔹 EDITAR
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    event = Event.query.get_or_404(id)

    if event.user_id != current_user.id:
        return redirect('/')

    if request.method == 'POST':
        event.title = request.form['title']
        event.description = request.form['description']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        event.time = datetime.strptime(request.form['time'], '%H:%M').time()

        db.session.commit()
        return redirect('/')

    return render_template('edit_event.html', event=event)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)