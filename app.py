import bcrypt
from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from forms import RegistrationForm, LoginForm, NoteForm
from models import db, User, Note
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
@login_required
def index():
    tag = request.args.get('tag')
    query = db.select(Note).filter_by(user_id=current_user.id)
    if tag:
        query = query.filter(Note.tags.ilike(f"%{tag}%"))
    notes = db.session.scalars(query.order_by(Note.created_at.desc())).all()
    return render_template('notes.html', notes=notes, current_tag=tag, tab='mine')

@app.route('/all_notes')
@login_required
def all_notes():
    tag = request.args.get('tag')
    query = db.select(Note)
    if tag:
        query = query.filter(Note.tags.ilike(f"%{tag}%"))
    notes = db.session.scalars(query.order_by(Note.created_at.desc())).all()
    return render_template('notes.html', notes=notes, current_tag=tag, tab='all')

@app.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        try:
            note = Note(
                title=form.title.data,
                content=form.content.data,
                tags=form.tags.data,
                user_id=current_user.id
            )

            db.session.add(note)
            db.session.commit()
            flash('Заметка успешно создана!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании заметки', 'error')
    return render_template('add_note.html', form=form)

@app.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    note = db.session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        abort(404)
    return render_template('note_detail.html', note=note)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            user = User(username=form.username.data, email=form.email.data, password=hashed_password.decode('utf-8'))
            db.session.add(user)
            db.session.commit()
            flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username или email уже существуют', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при регистрации', 'error')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).filter_by(username=form.username.data))
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/delete_note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = db.session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Заметка успешно удалена', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")
