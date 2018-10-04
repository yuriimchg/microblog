# Rendering the webpage
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post
# flash is to show messages to the user
# redirect is to redirect user from login page
# url_for is to create internal links painless
from flask import flash, redirect, url_for, render_template, request
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=["GET","POST"])
@app.route('/index', methods=["GET","POST"])
@login_required
def index():
    # Get the form
    form = PostForm()
    # On submitting the form...
    if form.validate_on_submit():
        # Add the new post
        post = Post(body=form.post.data, author=current_user)
        # Add the new post to the database
        db.session.add(post)
        # Commit changes to the database
        db.session.commit()
        flash('Well Done! You have posted it!')
        return redirect(url_for('index'))
    # List the following posts
    posts = current_user.followed_posts().all()
    page = request.args.get('page', 1, type=int)
    # View the posts
    posts = current_user.followed_posts().paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items)

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
        return redirect(next_page)
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

@app.route('/user/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    # Get the form to change the profile information
    form = EditProfileForm(current_user.username)
    # Change profile information on submit
    if form.validate_on_submit():
        # Change nickname
        current_user.username = form.username.data
        # Change information about user
        current_user.about_me = form.about_me.data
        # Commit changes to datebase
        db.session.commit()
        # Print informational message
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    # On loading the form
    elif request.method == 'GET':
        # Show username in the string field
        form.username.data = current_user.username
        # Show data about user in the text area field
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    # Get info from the database about the user to follow
    user = User.query.filter_by(username=username).first()
    # Case, if there is no such a user
    if user is None:
        # Error message
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    # Prevent from following himself
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    # Follow the chosen user
    current_user.follow(user)
    # Commit changes to the database
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    # Get info about the user from database
    user = User.query.filter_by(username=username).first()
    # Case, is there is no such a user to unfollow
    if user is None:
        # Error message
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    # Prevent from unfollowing himself
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    # Unfollow the chosen user
    current_user.unfollow(user)
    # Commit changes to the database
    db.session.commit()
    # A message of confirmation
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/explore')
@login_required
def explore():
    # Get the first page
    page = request.args.get('page', 1, type=int)
    # Posts should have descending order, depending on timestamp
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
                        page, app.config['POSTS_PER_PAGE'], False)
    # Go to next page
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    # Go to the previous page
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template("index.html", title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)
