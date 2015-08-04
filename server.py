#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser, flask, logging, pymongo
from datetime import datetime
from flask import Flask, redirect, request


config = configparser.ConfigParser()
config.read('config.cf')


db = pymongo.MongoClient().digital_library


app = Flask('digital_library')


def render_template(template_name, **context):
    test_books = [
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
    test_context = {
        'user': {"name": "Иван Иванов", "booksCount": 12},
        'device': "terminal",
        'books': test_books,
        'booksLen': len(test_books),
        'recomendedBooks': test_books,
        'recomendedBooksLen': len(test_books),
    }
    return flask.render_template(
        template_name + '.html',
        **dict(context, template_name = template_name, **test_context)
    )


@app.route("/login")
def login():
    return render_template("login")


@app.route("/reg")
def reg():
    return render_template("registration")


@app.route("/")
def home():
    return render_template("home")


@app.route("/handed")
def handed():
    return render_template("handed")


@app.route("/books")
def books():
    return render_template("books")


@app.route("/operations")
def operations():
    return render_template("operations")


@app.route('/term', methods = ['POST'])
def terminal():
    form = request.form
    if form["type"] == "user":
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
    global db
    user = curentTerminalUser(terminal)
    if db.hands.find_one({'user': user, 'book': book}) is not None:
        db.hands.insert({
            "user": user,
            "book": book,
            "datetime": datetime.utcnow(),
        })
        db.journal.insert({
            "user": user,
            "book": book,
            "datetime" datetime.utcnow(),
            "action": "hand",
            })
        successBookHand(terminal, book)
    else:
        db.hands.remove({"user": user, "book": book})
        db.journal.insert({
            "user": user,
            "book": book,
            "datetime" datetime.utcnow(),
            "action": "return",
            })
        successBookReturn(terminal, book)


def main():
    logging.basicConfig(level = logging.DEBUG)
    app.run(host = config["Server"]["host"], debug = True)


if __name__ == '__main__':
    main()