from Login import LoginForm
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import render_template, redirect, Flask
from flask_login import login_user, LoginManager, login_required, logout_user
from Register import RegisterForm
from JobNew import NewJob
from EditJob import EJobs
from data.product import Products
from data.turbo import Turbo
import sqlite3

app = Flask(__name__)
log_mangr = LoginManager()
log_mangr.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init("db/data21.db")
if len(db_session.create_session().query(Turbo).all()) != 12:
    s = ["Вилка", "Тормоза", "Колеса", "Рама", "Седло", "Подседельный штырь", "Грипсы",
         "Рулевая колонка", "Трансмисия", "Вынос", "Руль", "Педали"]

    for zn in s:
        tur = Turbo()
        db_sess = db_session.create_session()
        tur.name = zn
        db_sess.add(tur)
        db_sess.commit()
else:
    sqlite3.connect("data21").cursor().execute("DELETE FROM Turbo WHERE id > 12")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def start_window():
    db_sess = db_session.create_session()
    turbo = db_sess.query(Turbo).all()
    prod = db_sess.query(Products).all()
    types = {name.id: name.name for name in turbo}
    return render_template('index.html', prod=prod, types=types)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")



@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/addJob", methods=["GET", "POST"])
def newJob():
    form = NewJob()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Jobs).filter(Jobs.job == form.job_title.data).first():
            return render_template("addJob.html", title="Add new job",
                                   form=form,
                                   message="Такая работа уже создана")
        job = Jobs(
            team_leader=form.team_leader_id.data,
            job=form.job_title.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template("addJob.html", title="Add new job", form=form)


@app.route("/product/<int:number_of_list>")
def edit(number_of_list):
    form = EJobs()
    db_sess = db_session.create_session()
    prod = db_sess.query(Products).filter(Products.id == number_of_list).first()
    return render_template("editJob.html", title="About", form=form, prod=prod)


@log_mangr.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
