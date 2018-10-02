# Rendering the webpage
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
# flash is to show messages to the user
# redirect is to redirect user from login page
# url_for is to create internal links painless
from flask import flash, redirect, url_for, render_template, request
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    # Create pseudo user Ivan
    user = {'username':'Йван'}
    # Render title and username into webpage
    posts = [
        {
            'author' : {'username': 'Cow'},
            'body' : 'Moo-oo-oo-oo-u!'
        },
        {
            'author' : {'username' : 'Serj Tankian'},
            'body' : 'Eating seeds is the best time activity'
        },
        {
            'author' : {'username' : 'Jason Stathem'},
            'body' : 'I posted my first quotation to MDK when I was 16'
        }
    ]
    return render_template('index.html',
                            title='Home',
                            posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect authenticated users from login page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Initialize login form
    form = LoginForm()
    # Press the button 'Log in'
    if form.validate_on_submit():
    # Case of successful logging in
        user = User.query.filter_by(username=form.username.data).first()
        # Case of wrong nickname / password
        if user is None or not user.check_password(form.password.data):
            # Output message
            flash('Invalid username or password. Please enter the valid name and password')
            # Redirect to login page
            return redirect(url_for('login'))
        # Authentication process
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        # Case if there is no next page or next page is outside the microblog
        if not next_page or url_parse(next_page).netloc != '':
            # Let 'index' be the next page
            next_page = url_for('index')
        return redirect(url_for('index'))
    # Case of wrong login / password
    return render_template('login.html',
                            title='Sign In',
                            form=form)

# Log out the user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Registration page
@app.route('/register', methods=["GET", "POST"])
def register():
    # Redirect registered users to the main page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Initialize the form
    form = RegistrationForm()
    # On submitting the registration with registration forn
    if form.validate_on_submit():
        # Add user, email and password to the database
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # Add and commit changes to the database
        db.session.add(user)
        db.session.commit()
        # Successful registration message
        flash(f'Congratulations, {user.username}, you have successfully registered!\n Please sign in!')
        # Redirect to login page
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)

# User home page
@app.route('/user/<username>')
@login_required
def user(username):
    # Get user from the database by username. If there is no such a user, output 404
    user = User.query.filter_by(username=username).first_or_404()
    # User posts
    posts = [
            {'author':user, 'body':'Test post #1'},
            {'author':user, 'body':'Test post #2'}
        ]

    return render_template('user.html', user=user, posts=posts)
