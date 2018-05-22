# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, flash, jsonify, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, SendBattleForm
from app.models import User, Fight


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           users=User.get_top_users(5))


@app.route('/leaders')
def leaders():
    return render_template("leaders.html", title="Leadersboard",
                           users=User.get_top_users(50))


@app.route('/play')
@login_required
def play():
    return render_template("play.html", title="Free Play",
                           users=User.get_top_users(5))


@app.route('/fights', methods=['GET', 'POST'])
@login_required
def fights():
    form = SendBattleForm()
    if form.validate_on_submit():
        user = User.query.filter(User.id == form.user_id.data, User.name == form.username.data).first()
        if user is None:
            flash('Invalid Username and User ID')
        elif user == current_user:
            flash('You CAN NOT battle yourself')
        else:
            new_fight = Fight(current_user, user, status="friendly")
            db.session.add(new_fight)
            db.session.commit()
            flash('New fight!')
        return redirect(url_for('fights'))
    return render_template("fights.html", title="Fights", form=form,
                           fights=current_user.get_fights("friendly").all())


@app.route('/fight/<fid>')
@login_required
def play_fight(fid):
    fight = Fight.query.get_or_404(fid)
    if fight not in current_user.get_new_fights("friendly").all():
        abort(403)
    return render_template("play.html", title="Fight-{0}".format(fid),
                           users=fight.get_users(),
                           scores=fight.get_scores())


@app.route('/tournaments')
def tournaments():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/set_score', methods=['POST'])
@login_required
def set_score():
    data = request.json
    if data["from_url"] == "/play":
        current_user.set_score(int(data["score"]))
    elif int(data["from_url"].split("/")[2]) in [f.id for f in current_user.get_fights().all()]:
        Fight.query.get(int(data["from_url"].split("/")[2])).set_score(current_user, data["score"])
        current_user.set_score(int(data["score"]))
    db.session.commit()
    return jsonify({})
