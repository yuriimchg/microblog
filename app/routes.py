from app import app
from flask import render_template

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
