from datetime import datetime
import pytz
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import IndexForm, LoginForm, RegistrationForm, AssignmentForm, AssignmentButton
from app.models import User, Assignment, Task

date_format = '%Y-%m-%d %H:%M:%S'

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    button = AssignmentButton()

    assignments = current_user.assignments.all()
    tasks = current_user.tasks.all()
        
    if button.validate_on_submit():
        return redirect(url_for('create_assignment'))

    return render_template('index.html', title = 'Home', assignments = assignments,  button = button)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/create_assignment', methods = ['GET', 'POST'])
@login_required
def create_assignment():
    form = AssignmentForm()

    if form.validate_on_submit():
        print(type(form.due_date.data))
        f_date = str(form.due_date.data) + " "  + str(form.due_time.data)
        print(f_date)
        dt = datetime.strptime(f_date, date_format)
        timezone = pytz.timezone('Etc/Greenwich')
        d_aware = timezone.localize(dt)
        d_aware.tzinfo
        print(dt)


        assignment = Assignment(
            class_name = form.class_name.data,
            title = form.title.data,
            summary = form.summary.data,
            due = dt,
            creator = current_user 
        )

        db.session.add(assignment)
        db.session.commit()
        flash('Your assignment is posted!')
        return redirect(url_for('index'))

    return render_template('assignment.html', title = 'New Assignment', form = form)