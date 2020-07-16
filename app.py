from flask import Flask, render_template, request, redirect, url_for, logging, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key='Not Verified'

# the database
app.config['SQLALCHEMY_DATABASE_URI']='mysql://sql7338326:HSK4Tc5rDS@sql7.freemysqlhosting.net/sql7338326'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Users(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	nom=db.Column(db.String(20))
	prenom=db.Column(db.String(20))
	tel_mobile=db.Column(db.Integer)
	mail=db.Column(db.String(20),unique=True)
	mdp=db.Column(db.String(20))
	date_naissence=db.Column(db.DateTime)
	

class Passengers(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	id_user=db.Column(db.Integer,db.ForeignKey('users.id'))

class Drivers(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	id_user=db.Column(db.Integer,db.ForeignKey('users.id'))

# index form
@app.route('/')
def index():
	return render_template('index.html')

#register form
@app.route('/create', methods=['GET', 'POST'])
def create():
	if request.method =="POST" :
		nom=request.form['first_name']
		prenom=request.form['last_name']
		tel_mobile=request.form['phone_number']
		mail=request.form['email']
		mdp=request.form['Password']
		date_naissence=request.form['birthday']
		secure_password=sha256_crypt.encrypt(str(mdp))
		if ((nom!="") and (prenom!="") and (len(tel_mobile)==8) and (mail!="") and (mdp!="") and (date_naissence!="")):
			user=Users(nom=nom,prenom=prenom,tel_mobile=tel_mobile,mail=mail,mdp=mdp,date_naissence=date_naissence)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('trajet'))
		else:
			flash('Please verify that all your inputs all valid...')
			return render_template('create.html')

	return render_template('create.html')

#login form
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method =="POST" :
		mail=request.form['email']
		mdp=request.form['pass']

		mailData=Users.query.filter(Users.mail==mail,Users.mdp==mdp).first()


		if (mailData == ''):
			flash('Please verify your E-mail or password')
			return render_template('login.html')
		else:
			return redirect(url_for('trajet'))
			

	return render_template('login.html')


#creer un trajet
@app.route('/trajet', methods=['GET', 'POST'])
def trajet():
	if request.method =="POST" :
		Var=request.form.get('driver')
		if  Var== 'Driver':
			driver=Drivers(id_user=1)
			db.session.add(driver)
			db.session.commit()
			return redirect(url_for('driver'))
		else:
			passenger=Passengers(id_user=1)
			db.session.add(passenger)
			db.session.commit()
			return redirect(url_for('passenger'))
	return render_template('trajet.html')

#passenger
@app.route('/passenger')
def passenger():
	return render_template('passenger_trajet.html')

#driver
@app.route('/driver')
def driver():
	return render_template('driver_trajet.html')
#contact
@app.route('/contact')
def contact():
	return render_template('contact.html')

#resultat
@app.route('/result')
def result():
	return render_template('result.html')

if __name__ == '__main__':
	app.run(debug=True)
	