#!/usr/bin/env python3'
from flask import Flask, render_template, redirect

app = Flask(__name__)

user = {"name": "Иван Иванов", "booksCount": 12}
devise = "terminal"

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/reg")
def reg():
	return render_template("reg.html")

@app.route("/")
def home():
	return render_template("home.html", title = "Главная", user = user, devise = devise)

@app.route("/myBooks")
def myBooks():
	return render_template("myBooks.html", title = "Мои книги", user = user, devise = devise)

@app.route("/books")
def books():
	return render_template("books.html", title = "Каталог", user = user, devise = devise)

@app.route("/handBooks")
def handBooks():
	return render_template("handBooks.html", title = "Взять книги", user = user, devise = devise)

@app.route("/returnBooks")
def returnBooks():
	return render_template("returnBooks.html", title = "Вернуть книги", user = user, devise = devise)

app.run(host="::", port=5000, debug=True)