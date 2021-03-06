import os
import time
import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from itsdangerous.url_safe import URLSafeSerializer


###########################
######### SET UP ##########
###########################

app = Flask(__name__)
app.secret_key = os.urandom(24)


# set up for cookie encryption
key = os.urandom(24)
cookie_encryptor = URLSafeSerializer(key)

# set up for SQL databese and database migration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLAHCHEMY_TRACK_MODIFICATION'] = False
app.config['JSON_AS_ASCII'] = False


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

### index page ###
@app.route('/', methods=['GET'])
def index():
    if "message" in session:
        flash_message = session['message']
        flash(flash_message)
        session.pop('message')
    return render_template('index.html')


### signup url, redirect to index page after storing user credential into DB ###
@app.route('/signup', methods=['POST'])
def signup():
    
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    
    if name and username and password:
    
        # check if username exist
        if User.query.filter_by(username=username).first():
            return redirect(url_for('error', message="?????????????????????"))
            
        else:
            
            new_user = User(name=name, username=username, password=password, time=datetime.datetime.now())
            
            db.session.add(new_user)
            db.session.commit()
            
            session['message'] = "?????????????????????????????????????????????"
            
            return redirect(url_for('index'))
    
    else:
        session['message'] = "?????????????????????"
        return redirect(url_for('index'))
    
### signin url, redirect to member/error page after checking credential in DB ###
@app.route('/signin', methods=['POST'])
def signin():

    username = request.form['username']
    password = request.form['password']
    
    if username and password:
    
        if User.query.filter_by(username=username).first():
        
            user = User.query.filter_by(username=username).first()
            
            if user.password.decode('utf-8') == password:
                res = make_response(redirect(url_for('member')))
                res.set_cookie(key='sessionID',
                               value=cookie_encryptor.dumps(username),
                               expires=time.time() + 5 * 60)
                return res
            else:
                return redirect(url_for('error', message="???????????????????????????"))
            
        else:
            return redirect(url_for('error', message="???????????????????????????"))
    
    else:
        session['message'] = "?????????????????????"
        return redirect(url_for('index'))

### error page ###
@app.route('/error/', methods=['GET'])
def error():
    return render_template('error.html', error_message=request.args.get('message'))

### member page (check if user logged in) ###
@app.route('/member/')
def member():
    session_id = request.cookies.get('sessionID')
    if session_id and User.query.filter_by(username=cookie_encryptor.loads(session_id)).first():
        return render_template('member.html')
    else:
        session['message'] = "??????????????????"
        return redirect(url_for('index'))


### signout url, modify session and redirect to index page ###
@app.route('/signout')
def signout():
    session_id = request.cookies.get('sessionID')
    
    if session_id and User.query.filter_by(username=cookie_encryptor.loads(session_id)).first():
        res = make_response(redirect(url_for('index')))
        session['message'] = "??????????????????"
        res.set_cookie(key='sessionID',value='', expires=0)
        return res
    
    else:
        return redirect(url_for('index'))
    
    
    
#########################
########## API ##########
#########################

##### api for getting specified other user's info #####
@app.route('/api/users', methods=['GET'])
def inquire_user():
    
    session_id = request.cookies.get('sessionID')
    
    if session_id and User.query.filter_by(username=cookie_encryptor.loads(session_id)).first():
        username_to_get = request.args.get('username')
    
        if User.query.filter_by(username=username_to_get).first():
            
            user_to_get = User.query.filter_by(username=username_to_get).first()
            
            response = {
                "data":{
                    "id":user_to_get.id,
                    "name":user_to_get.name, 
                    "username":user_to_get.username.decode('utf-8')
                }
            }
        else:
            response = {
                "data": None
            }

        return jsonify(response)
    
    else:
        return "?????????????????????????????????"

##### api for update user's name #####
@app.route('/api/user', methods=['POST'])
def change_name():
    session_id = request.cookies.get('sessionID')
    if session_id and User.query.filter_by(username=cookie_encryptor.loads(session_id)).first():
    
        req = request.get_json();
        new_name = req['name']
        
        user = User.query.filter_by(username=cookie_encryptor.loads(session_id)).first()
        user.name = new_name
        try:
            db.session.add(user)
            db.session.commit()
            session['name'] = new_name
            response = make_response(jsonify({
                "ok":True
            }),200)
            return response
        except:
            response = make_response(jsonify({
                "error":True
            }),200)
            return response
    else:
        return "???????????????????????????????????????"

##### api for retriving user's own name #####
@app.route('/api/user', methods=['GET'])
def get_user():
    session_id = request.cookies.get('sessionID')
    if session_id and User.query.filter_by(username=cookie_encryptor.loads(session_id)).first():
        user = User.query.filter_by(username=cookie_encryptor.loads(session_id)).first()
        
        response = {
            "data":{
                "id":user.id,
                "name":user.name,
                "username": user.username.decode('utf-8')
            }
        }
        return jsonify(response)
    
    return "?????????????????????????????????"
        


if __name__ == '__main__':
    app.run(port=3000,debug=True)
    