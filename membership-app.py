import os
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime


###########################
######### SET UP ##########
###########################

app = Flask(__name__)
app.secret_key = os.urandom(24)

# set up for SQL databese and database migration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sontforg123@localhost/website'
app.config['SQLAHCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app,db)


###########################
### Define Model(table) ###
###########################

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255,collation='binary'), nullable=False)
    password = db.Column(db.String(255,collation='binary'), nullable=False)
    time = db.Column(db.DateTime)
    
    def __init__(self,name,username,password,time):
        self.name = name
        self.username = username
        self.password = password
        self.time = time


######################
### view functions ###
######################

@app.route('/', methods=['GET'])
def index():
    if "message" in session:
        flash_message = session['message']
        flash(flash_message)
        session['message'] = ''
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
     
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    
    if User.query.filter_by(username=username).first():
        return redirect(url_for('error', message="此帳號已被註冊"))
        
    else:
        
        new_user = User(name=name, username=username, password=password, time=datetime.datetime.now())
        
        db.session.add(new_user)
        db.session.commit()
        
        session['message'] = "您已完成註冊，請用帳號密碼登入"
        
        return redirect(url_for('index'))
    

@app.route('/signin', methods=['POST'])
def signin():

    username = request.form['username']
    password = request.form['password']
    
    if User.query.filter_by(username=username).first():
    
        user = User.query.filter_by(username=username).first()
        
        if user.password.decode('utf-8') == password:
            session['status'] = "已登入"
            session['name'] = user.name
            return redirect(url_for('member'))
        else:
            return redirect(url_for('error', message="帳號或密碼輸入錯誤"))
        
    else:
        return redirect(url_for('error', message="帳號或密碼輸入錯誤"))


@app.route('/error/', methods=['GET'])
def error():
    return render_template('error.html', error_message=request.args.get('message'))


@app.route('/member/')
def member():
    if session['status'] and session['status'] == '已登入':
        return render_template('member.html')
    else:
        return redirect(url_for('index'))


@app.route('/signout')
def signout():
    if not session['status']:
        return redirect(url_for('index'))
    elif session['status'] == '已登入':
        session['status'] = None
        session['name'] = ''
        session['message'] = "您已成功登出"
        return redirect(url_for('index'))
    
    

if __name__ == '__main__':
    app.run(port=3000,debug=True)
    