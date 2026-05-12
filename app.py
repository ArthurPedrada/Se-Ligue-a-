from flask import Flask, render_template, request, redirect
from models import db, Event
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Criar banco (apenas no início)
with app.app_context():
    db.create_all()


# 🔹 Página principal (RF03)
@app.route('/')
def agenda():
    events = Event.query.order_by(Event.date, Event.time).all()
    return render_template('agenda.html', events=events)


# 🔹 Criar evento (RF02)
@app.route('/create', methods=['POST'])
def create():
    event = Event(
        title=request.form['title'],
        description=request.form['description'],
        date=request.form['date'],
        time=request.form['time']
    )

    db.session.add(event)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)