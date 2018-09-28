# Rendering the webpage
from flask import render_template
from app import app
from app.forms import LoginForm
# flash is to show messages to the user
# redirect is to redirect user from login page
# url_for is to create internal links painless
from flask import flash, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
    # Create pseudo user Ivan
    user = {'username':'Йван'}
    # Render title and username into webpage
    posts = [
        {
            'author' : {'username': 'John Price'},
            'body' : 'Cheeky bastard'
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
                            user=user,
                            posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Initialize login form
    form = LoginForm()
    #
    if form.validate_on_submit():
        # Case of successful logging in
        flash(f'Login requested for user {form.username.data}, Remember me: {form.remember_me.data}')
        return redirect(url_for('/index'))

    # Case of wrong login / password
    return render_template('login.html',
                            title='Sign In',
                            form=form)
