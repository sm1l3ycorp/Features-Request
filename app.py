from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///features.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #FSADeprecationWarning
app.config['SECRET_KEY'] = "burger time"
db = SQLAlchemy(app)

class featureR(db.Model):
	id = db.Column('feature_id', db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	description = db.Column(db.String(300), nullable=False)
	client = db.Column(db.String(8), nullable=False) 
	clientPriority = db.Column(db.Integer, nullable=False)
	targetDate = db.Column(db.String(10), nullable=False)
	productArea = db.Column(db.String(8), nullable=False)
   
	def __init__(self, title, description, client, clientPriority, targetDate, productArea):
		self.title = title
		self.description = description
		self.client = client
		self.clientPriority = clientPriority
		self.targetDate = targetDate
		self.productArea = productArea

@app.route('/')
def view():
   return render_template('index.html', feature = featureR.query.all() )

@app.route('/', methods = ['GET', 'POST'])
def create():
   if request.method == 'POST':
      if not request.form['title'] or not request.form['description'] or not request.form['client'] or not request.form['clientPriority'] or not request.form['targetDate'] or not request.form['productArea']:
         flash('Please enter all the fields', 'error')
      else:
         feature = featureR(request.form['title'], request.form['description'],
		 request.form['client'], request.form['clientPriority'],
		 request.form['targetDate'], request.form['productArea'] )
         
         db.session.add(feature)
         db.session.commit()
         flash('Feature requested!')
         return redirect(url_for('view'))
   return render_template('index.html')

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)