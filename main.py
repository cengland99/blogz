from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz1@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    entry = db.Column(db.String(240))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, entry, owner):
        self.name = name
        self.entry = entry
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.route('/')
def index():
    
    id_exists = request.args.get('id')
    if id_exists:
        single_blog = Blog.query.filter_by(id = id_exists).first()
        return render_template('single.html', blog=single_blog)
    else:   
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)


@app.route('/new', methods=['POST', 'GET'])
def new_post():

    if request.method == 'GET':
        return render_template('new.html')

    elif request.method == 'POST':
        name = request.form['name']
        entry = request.form['entry']
        name_error = ''
        entry_error = ''

        if "" == name:
            name_error = 'Title is required!'
            name = ''
        if "" == entry:
            entry_error = 'Body is required!'
            entry = ''
    
        if name_error or entry_error:
            return render_template('new.html', name=name, entry=entry, name_error=name_error, entry_error=entry_error)

        else:
            new_blog = Blog(name,entry)
            name = request.form['name']
            entry = request.form['entry']
            
            db.session.add(new_blog)
            db.session.commit()
            blog = Blog.query.filter_by(name=name).first()
            return render_template('single.html', blog=blog)
    
        
            

    



if __name__ == '__main__':
    app.run()
