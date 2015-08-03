#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, request
import configparser, pymongo

config = configparser.ConfigParser()
config.read('config.cf')

base = pymongo.MongoClient()
users = base.digital_library.users
books = base.digital_library.books
hands = base.digital_library.hands
tags = base.digital_library.tags

app = Flask(__name__)

user = {"name": "Иван Иванов"}
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
booksLen = len(booksList)

@app.route("/login")
def login():
	return render_template("login.html", devise = devise)

@app.route("/reg")
def reg():
	return render_template("reg.html")

@app.route("/")
def home():
	return render_template(
		"home.html",
		title = "Главная", 
		user = user, 
		devise = devise, 
		recBooks = recBooksList, 
		books = booksList, 
		booksLen = booksLen
		)

@app.route("/handed")
def handed():
	return render_template(
		"handed.html", 
		title = "Мои книги", 
		user = user, 
		devise = devise, 
		books = booksList, 
		booksLen = booksLen
		)

@app.route("/books")
def books():
	return render_template(
		"books.html", 
		title = "Каталог", 
		user = user, 
		devise = devise, 
		books = booksList, 
		booksLen = booksLen
		)

@app.route("/operations")
def operations():
	return render_template(
		"operations.html", 
		title = "Взять/Вернуть книги", 
		user = user, 
		devise = devise, 
		books = booksList, 
		booksLen = booksLen
		)

@app.route('/term', methods=['POST'])
def tarminal():
	form = request.form
	if(form["type"] == "user"):
		newTerminalUser(form["id"], form["data"])
		return ""
	else:
		userBookOperation(form["id"], form["data"])
		return ""

def newTerminalUser(terminal, user):
	pass

def curentTerminalUser(terminal):
	return "testUser"

def successBookHand(terminal, book):
	pass

def successBookReturn(terminal, book):
	pass

def userBookOperation(terminal, book):
	global hands, books
	if(list(hands.find({"user": curentTerminalUser(terminal)})) == []):
		hands.insert({"user": curentTerminalUser(terminal), "book": book, "time": time.ctime(time.time()), "status": "on"})
		books.update({"_id": book}, {"$set": {"handed": int(books.find_one({"_id": book_id})["handed"]) + 1}})
		successBookHand(terminal, book)
	else:
		hands.update({"user": curentTerminalUser(terminal), "book": book}, {"$set": {"status": "off"}})
		books.update({"_id": book}, {"$set": {"handed": int(books.find_one({"_id": book_id})["handed"]) - 1}})
		successBookReturn(terminal, book)

app.run(host = config["Server"]["host"], port = 5000, debug = True)