#!/usr/bin/env python3
from flask import Flask, render_template, redirect

app = Flask(__name__)

user = {"name": "Иван Иванов", "booksCount": 4}
devise = "terminal"
booksList = [
	{
		"title" : "Что такое математика?",
		"author": "Р. Курант, Г. Роббинс",
		"image": "http://math4school.ru/img/math4school_ru/books/book_review_002.jpg",
	}, 
	{
		"title" : "Сборник задач по алгебре",
		"author": "М.Л. Галицкий, А.М. Гольдман, Л.И. Звавич",
		"image": "http://static.my-shop.ru/product/2/1/8224.jpg",
	}, 
	{
		"title" : "Алгоритмы: построение и анализ",
		"author": "К. Штайн, Р. Линн Ривест, Т. Кормен, Ч. Эрик Лейзерсон",
		"image": "http://bookimir.ru/uploads/posts/2014-03/thumbs/1395595379_pzrkjqvsr9nihts.jpeg",
	},
	{
		"title" : "Совершенный код",
		"author": "С. Макконнелл",
		"image": "http://s4.goods.ozstatic.by/200/206/15/1/1015206_0_Sovershenniy_kod_Master-klass_Stiv_MakKonnell.jpg",
	},
]

recBooksList = booksList

@app.route("/login")
def login():
	return render_template("login.html", devise = devise)

@app.route("/reg")
def reg():
	return render_template("reg.html")

@app.route("/")
def home():
	return render_template("home.html", title = "Главная", user = user, devise = devise, recBooks = recBooksList)

@app.route("/myBooks")
def myBooks():
	return render_template("myBooks.html", title = "Мои книги", user = user, devise = devise, books = booksList)

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