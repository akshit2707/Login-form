from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt

engine=create_engine("mysql+pymysql://root:1234567@localhost/register")  
db=scoped_session(sessionmaker(bind=engine))
app=Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")


@app.route("/register",methods=["GET","POST"])
def register():
	if request.method=="POST":
		name=request.form.get("name")
		username=request.form.get("username")
		password=request.form.get("password")
		confirm=request.form.get("confirm")
		secure_password=sha256_crypt.encrypt(str(password))


		if(password==confirm):
			db.execute("INSERT INTO users(name,username,password) VALUES(:name,:username,:password)",{"name":name,"username":username,"password":secure_password})
			db.commit()
			flash("You are registered and can login", "success")
			return redirect(url_for('login'))
		else:
			flash("Password does not match","danger")
			return render_template("register.html")
	return render_template("register.html")


@app.route("/login",methods=["GET","POST"])
def login():
	if request.method=="POST": 
		username=request.form.get("name")
		password=request.form.get("password")

		usernamedata=db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
		passworddata=db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()

		if usernamedata is None:
			flash("No username","danger")
			return render_template("login.html")
		else:
			for passwor_data in passwordata:
				if sha256_crypt.verify(password,passwor_data):
					session["log"]=True

					flash("You are now login","success")
					return redirect(url_for('hey'))
				else:
					flash("INCORRECT PASSWORD","danger")
					return render_template("login.html")

	return render_template("login.html")

@app.route("/hey")
def hey():
	return render_template("hey.html")

@app.route("/logout")
def logout():
	session.clear()
	flash("You are now loged out","success")
	return redirect(url_for('login'))
if (__name__)==("__main__"):
	app.secret_key="1234567akshit"
	app.run(debug=True)
