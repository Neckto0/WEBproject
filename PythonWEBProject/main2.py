from forms.Login import LoginForm
from data import db_session, users_api, prod_api
from data.users import User
from flask import render_template, redirect, Flask, Blueprint, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms.Register import RegisterForm
from forms.JobNew import NewJob
from forms.EditJob import EJobs
from data.product import Products
from data.turbo import Turbo
from forms.filters import Filter
from forms.Code import Codes
from forms.cart import Card
from forms.profile import Profile
from forms.recovery import Recov
from forms.EditPassword import EditPass
from random import randint
import sqlite3
import smtplib
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
log_mangr = LoginManager()
log_mangr.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD'] = os.path.join("static", 'Picture')

prod_bl_print = Blueprint(
    "products",
    __name__,
    template_folder="templates"
)


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

    user2 = db_sess.query(User).filter(User.code != 0).all()
    for user in user2:
        ust = db_sess.query(User).filter(User.id == user.id).first()
        ust.code = 0
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
    a = {1: filter_form.fork.data, 2: filter_form.breakers.data, 3: filter_form.wheels.data,
         4: filter_form.frame.data, 5: filter_form.saddle.data, 6: filter_form.saddle_post.data,
         7: filter_form.grips.data, 8: filter_form.steering_colm.data,
         9: filter_form.transmission.data, 10: filter_form.stem.data, 11: filter_form.bar.data,
         12: filter_form.pedals.data}
    db_sess = db_session.create_session()
    turbo = db_sess.query(Turbo).all()
    prod = db_sess.query(Products).all()
    types = {name.id: name.name for name in turbo}
    if filter_form.submit.data:
        s = []
        prod2 = []
        for typ in a.keys():
            if a[typ]:
                s.append(typ)
        if int(filter_form.max.data) != 0 or int(filter_form.min.data) != 0:
            for i in s:
                prod1 = db_sess.query(Products).filter(Products.type == i and
                                                       int(filter_form.max.data) >= Products.price >= int(filter_form.min.data)).all()
                for kop in prod1:
                    if int(filter_form.max.data) != 0:
                        if kop.type == i and int(filter_form.max.data) >= kop.price >= int(filter_form.min.data):
                            prod2.append(kop)
                    else:
                        if kop.type == i and kop.price >= int(filter_form.min.data):
                            prod2.append(kop)
        else:
            for i in s:
                prod1 = db_sess.query(Products).filter(Products.type == i).all()
                for kop in prod1:
                    prod2.append(kop)
        if all(not element for i, element in a.items()):
            if filter_form.max.data or filter_form.min.data:
                prods = db_sess.query(Products).all()
                if int(filter_form.max.data) != 0:
                    prod1 = [m for m in prods if int(filter_form.max.data) >= m.price >= int(filter_form.min.data)]
                else:
                    prod1 = [m for m in prods if m.price >= int(filter_form.min.data)]
                return render_template('index.html', prod=prod1, types=types, form=filter_form,
                                       message=f"найдено {len(prod1)} результатов")
            else:
                return render_template('index.html', prod=prod, types=types, form=filter_form,
                                       message=f"найдено {len(prod)} результатов")
        return render_template('index.html', prod=prod2, types=types, form=filter_form,
                               message=f"найдено {len(prod2)} результатов")
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


@app.route("/Delprod/<int:id>")
def deleteb(id):
    db_sess = db_session.create_session()
    pop = db_sess.query(Products).filter(Products.id == id).first()
    if os.path.exists(f"static/{pop.picture}"):
        os.remove(f"static/{pop.picture}")
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


@app.route("/adddet", methods=["GET", "POST"])
def newdet():
    form = NewJob()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Products).filter(Products == form.det_titl.data).first():
            return render_template("addJob.html", title="Add new detal",
                                   form=form,
                                   message="Такая деталь уже создана")
        prod = Products(
            name=form.det_titl.data,
            type=form.type.data,
            quality=form.qual.data,
            price=form.price.data,

        )
        file = request.files["pic"]
        prod.picture = f"Picture/{file.filename}"
        file.save(os.path.join(app.config['UPLOAD'], secure_filename(file.filename)))
        db_sess.add(prod)
        db_sess.commit()
        return redirect("/")
    return render_template("addJob.html", title="Add new product", form=form)


@app.route('/deletefromcard/<int:id>')
def delfromcard(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    s = [int(i) for i in user.basket.split(', ')]
    del s[s.index(id)]
    if s:
        user.basket = ", ".join([str(i) for i in s])
    else:
        user.basket = None
    db_sess.commit()
    return redirect('/cart')


@app.route("/cart", methods=["GET", "POST"])
def cart():
    db_sess = db_session.create_session()
    turbo = db_sess.query(Turbo).all()
    us = db_sess.query(User).filter(User.id == current_user.id).first()
    products_in_card = []
    if us.basket:
        s = [i for i in us.basket.split(", ")]
    else:
        s = []
    db_sess.commit()
    form = Card()
    types = {name.id: name.name for name in turbo}
    if s:
        products_in_card = [db_sess.query(Products).filter(Products.id == int(i)).first() for i in s]
        return render_template("cart.html", db=db_sess, user=User,
                               form=form, prod=products_in_card, type=types, spis=s)
    return render_template("cart.html", db=db_sess, user=User,
                           form=form, prod=products_in_card, type=types, spis=s,
                           message="Добавьте что-нибудь в корзину, чтобы она не была пуста")


@app.route("/addtocard/<int:id>", methods=["GET", "POST"])
def addcard(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user.basket:
        s = [int(i) for i in user.basket.split(", ")]
        s.append(id)
        user.basket = ", ".join([str(i) for i in s])
    else:
        user.basket = id
    db_sess.commit()
    return redirect("/")


@app.route("/product/<int:number_of_list>")
def edit(number_of_list):
    form = EJobs()
    db_sess = db_session.create_session()
    prod = db_sess.query(Products).filter(Products.id == number_of_list).first()
    return render_template("editJob.html", title="About", form=form, prod=prod)


@app.route("/buy")
def buy():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    prod = db_sess.query(Products).all()
    s = [m for m in prod if m.id in [int(i) for i in user.basket.split(", ")]]
    spi = [f'{m[0]} {m[1]}RUB\n' for m in [[i.name, i.price] for i in s]]
    sum_all = sum([i.price for i in s])
    for pro in s:
        pro.product_quantity -= 1
        db_sess.commit()
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.starttls()
    smtpObj.login("site0mtb@gmail.com", "xuhd ycre lmdp pvoz")
    smtpObj.sendmail("site0mtb@gmail.com", user.email,
                     '\n'.join(spi) + f"\nTotal: {sum_all} RUB")
    smtpObj.quit()
    user.basket = None
    db_sess.commit()
    return render_template("Buy.html")


@app.route("/profile", methods=["GET", "POST"])
def prof():
    form = Profile()
    if form.submit.data:
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.id == current_user.id).first()
        users.name = form.name.data
        users.about = form.about.data
        db_sess.commit()
        return redirect("/profile")
    return render_template("profile.html", form=form)


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    form = Recov()
    if form.submit.data:
        db_sess = db_session.create_session()
        users = [i.email for i in db_sess.query(User).all()]
        if form.email.data in users:
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            user.code = randint(100000, 999999)
            db_sess.commit()
            return redirect("/recovery/next")
        return render_template("recovery.html", form=form, message="Такого пользователя нет")
    return render_template('recovery.html', form=form)


@app.route("/recovery/next", methods=["GET", "POST"])
def nextrev():
    form = Codes()
    db_sess = db_session.create_session()
    us = db_sess.query(User).filter(User.code != 0).first()
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.starttls()
    smtpObj.login("site0mtb@gmail.com", "xuhd ycre lmdp pvoz")
    smtpObj.sendmail("site0mtb@gmail.com", us.email, f"Hello, this your code {us.code}")
    if form.submit.data:
        if form.code.data == str(us.code):
            return redirect("/recovery/edit")
        return render_template("Code.html", form=form, email=us.email, message="Код неверный")
    return render_template("Code.html", form=form, email=us.email)


@app.route("/recovery/edit", methods=["GET", "POST"])
def editaccount():
    form = EditPass()
    if form.submit.data:
        if form.password.data != form.password_ag.data:
            print(form.password.data, form.password_ag.data)
            return render_template("editPassword.html", form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        us = db_sess.query(User).filter(User.code != 0).first()
        us.set_password(form.password.data)
        db_sess.commit()
        return redirect("/login")
    return render_template("editPassword.html", form=form)


@log_mangr.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    create()
    app.register_blueprint(users_api.us_bl_print)
    app.register_blueprint(prod_api.prod_bl_print)
    app.run()


if __name__ == '__main__':
    main()
