#!/usr/bin/env python3'
from flask import Flask, render_template, redirect

app = Flask(__name__)

user = {"name": "Иван Иванов", "booksCount": 12}

@app.route("/")
def home():
	return render_template("home.html", title = "Мои книги", user = user)

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/reg")
def reg():
	return render_template("reg.html")

app.run(host="::", port=5000, debug=True)