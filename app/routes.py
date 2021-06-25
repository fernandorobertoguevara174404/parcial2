from flask import render_template, flash, redirect, url_for
from app import app, db, flask_uuid
from app.forms import LoginForm, SignUpForm, NotaForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Note
import uuid

@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        #POST
        #Iniciar sesión con base de datos
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("No se encontro el usuario o la contraseña esta incorrecta")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash("Iniciaste Sesión correctamente, Hola {}".format(form.username.data))
        return redirect("/index")
    return render_template("login.html", title="Login",form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(form)
        if user is None:
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Usuario creado exitosamente")

        else:
            flash("El usuario ya existe")
            return redirect(url_for("signup"))
        
        
        return redirect("/index")
    return render_template("signup.html", title="Signup",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/notas", methods=["GET"])
@login_required
def notas_index():
    notas = Note.query.filter_by(users_id=current_user.id).all()
    return render_template("notas_index.html",notas = notas)

@app.route("/notas/<int:id>")
@login_required
def notas_show(id,id_uuid):
    nota = Note.query.filter_by(id=id).first()
    return render_template("notas_show.html", nota=nota)

@app.route("/notas/create", methods=["GET", "POST"])
def notas_create():
    form=NotaForm()
    if form.validate_on_submit():
        nota = Note(name=form.name.data, body=form.body.data, users_id=current_user.id)
        db.session.add(nota)
        db.session.commit()
        return redirect(url_for("notas_index"))
    else:
        #pidiento el formulario
        return render_template("nota_create.html", form=form)

@app.route("/notas/destroy/<int:id>")
@login_required
def notas_destroy(id):
    nota = Note.query.filter_by(id=id).first()
    if nota and nota.users_id == current_user.id:
        db.session.delete(nota)
        db.session.commit()
    else:
        flash("No tienes permisos para eliminar este recurso")
    return redirect(url_for("notas_index"))
