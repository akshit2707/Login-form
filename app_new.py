from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin,AdminIndexView
from flask_login import UserMixin,LoginManager,current_user,login_user,logout_user
from flask_admin.contrib.sqla import ModelView

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql:///myadmin.db"
app.config['SECRET KEY']='mysecret'


db=SQLAlchemy(app)
login=LoginManager(app)

@login.user_loader
def load_user(user_id):
	return User.query.get(user_id)



class User(db.Model):
	id=db.Column(db.Integer,primary_key=True)
    #name=db.Column(db.String(20))

class Mymodel(ModelView):  #so that i could edit the function of ModelView and customize it as per requirement
	def is_access(self):
		return current_user.is_authenticated   # now the admin part is hidden in the loaclhost

	def inaccessible_callback(self,name):
		return redirect(url_for('login'))

class Myadminindexview(AdminIndexView):
	def is_access(self):
		return current_user.is_authenticated  #again hiding the details of the admin



admin=Admin(app,index_view=Myadminindexview())
admin.add_view(Mymodel(User,db.session))


@app.route('/login')
def login():
	user=User.query.get(1)
	login_user(user)
	return 'logged in'



if __name__=='__main__':
  	app.run(debug=True)