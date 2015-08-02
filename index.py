#!/usr/bin/env python3'
from flask import Flask, render_template, redirect

app = Flask(__name__)

user = {"name": "Иван Иванов", "booksCount": 12}

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/reg")
def reg():
	return render_template("reg.html")

@app.route("/")
def home():
	return render_template("home.html", title = "Главная", user = user)

@app.route("/myBooks")
def myBooks():
	return render_template("myBooks.html", title = "Мои книги", user = user)

@app.route("/books")
def books():
	return render_template("books.html", title = "Каталог", user = user)

app.run(host="::", port=5000, debug=True)