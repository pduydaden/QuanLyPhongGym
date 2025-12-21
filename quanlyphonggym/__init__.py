
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost:3306/gymdb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db= SQLAlchemy(app)
