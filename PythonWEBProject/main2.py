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
from filters import Filter
from Code import Codes
from random import randint
import sqlite3
import smtplib

app = Flask(__name__)
log_mangr = LoginManager()
log_mangr.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def create():
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
        sqlite3.connect("db/data21.db").cursor().execute("DELETE FROM Turbo WHERE id > 12")


@app.route('/login', methods=['GET', 'POST'])
def login():
    db_sess = db_session.create_session()
    user1 = db_sess.query(User).filter(User.is_active == 0).all()
    for user in user1:
        pop = db_sess.query(User).filter(User.id == user.id).first()
        db_sess.delete(pop)
        db_sess.commit()

    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/', methods=["GET", "POST"])
def start_window():
    filter_form = Filter()
    a = {"fork": "Вилка", "breakers": "Тормоза", "wheels": "Колеса", "frame": "Рама",
         "saddle": "Седло", "saddle_post": "Подседельный штырь", "grips": "Грипсы",
         "steering_colm": "Рулевая колонка", "transmission": "Трансмисия", "stem": "Вынос",
         "bar": "Руль", "pedals": "Педали"}
    db_sess = db_session.create_session()
    turbo = db_sess.query(Turbo).all()
    prod = db_sess.query(Products).all()
    types = {name.id: name.name for name in turbo}
    if filter_form.validate_on_submit():
        s = []
        for typ in a.keys():
            eval(f"""if form.{typ}:
                            s.append(a[{typ}])""")
            prod = db_sess.query(Products).filter(Products.type in s).all()
        return render_template('index.html', prod=prod, types=types, form=filter_form, message=a)
    return render_template('index.html', prod=prod, types=types, form=filter_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/delete/<int:id>")
def deletea(id):
    logout_user()
    db_sess = db_session.create_session()
    pop = db_sess.query(User).filter(User.id == id).first()
    db_sess.delete(pop)
    db_sess.commit()
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
            about=form.about.data,
            is_active=0,
            code=randint(100000, 999999)
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect("/conf")
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/conf", methods=["POST", "GET"])
def code():
    form_code = Codes()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.is_active == 0).first()
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.starttls()
    smtpObj.login("site0mtb@gmail.com", "xuhd ycre lmdp pvoz")
    smtpObj.sendmail("site0mtb@gmail.com", user.email, f"Hello, this your code {user.code}")
    smtpObj.quit()
    if form_code.validate_on_submit():
        if form_code.code.data == str(user.code):
            user.is_active = 1
            user.code = 0
            db_sess.commit()
            return redirect("/login")
        else:
            return render_template("Code.html", form=form_code, email=user.email,
                                   message="Код не верный, проверьте код")
    return render_template("Code.html", form=form_code, email=user.email)


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
    create()
    app.run()


if __name__ == '__main__':
    main()
