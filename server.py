#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from datetime import datetime
from flask import Flask, jsonify, request
import flask
import logging
import pymongo
import requests
import uuid


app = Flask('digital_library')


def load_config():
    config = configparser.ConfigParser()
    config.read('config.cf')
    return config['Server']


def open_db():
    return pymongo.MongoClient().digital_library


def dbTerminalsInsert(client_ip, terminal_uuid):
    global db
    db.terminals.insert({"ip": client_ip, "uuid": str(terminal_uuid)})


def dbTerminalsFind(client_ip):
    global db
    return db.terminals.find_one({'ip': client_ip})


def dbTerminalsFindUUID(client_ip):
    global db
    terminal_uuid = db.terminals.find_one({'ip': client_ip})["uuid"]
    return terminal_uuid


def dbHandsInsert(user, book):
    global db
    now = datetime.utcnow()
    db.hands.insert({
        "user": user,
        "book": book,
        "datetime": now,
    })


def dbHandFind(user, book):
    global db
    return db.hands.find_one({'user': user, 'book': book})


def dbHandsRemove(user, book):
    global db
    db.hands.remove({"user": user, "book": book})


def dbJournalInsert(user, book, action):
    global db
    now = datetime.utcnow()
    db.journal.insert({
        "user": user,
        "book": book,
        "datetime": now,
        "action": action,
    })


def render_template(template_name, **context):
    test_books = [
        {
            "title": "Что такое математика?",
            "author": "Р. Курант, Г. Роббинс",
            "image": "http://math4school.ru/img/math4school_ru/books/book_review_002.jpg",
        },
        {
            "title": "Сборник задач по алгебре",
            "author": "М.Л. Галицкий, А.М. Гольдман, Л.И. Звавич",
            "image": "http://static.my-shop.ru/product/2/1/8224.jpg",
        },
        {
            "title": "Алгоритмы: построение и анализ",
            "author": "К. Штайн, Р. Линн Ривест, Т. Кормен, Ч. Эрик Лейзерсон",
            "image": "http://bookimir.ru/uploads/posts/2014-03/thumbs/1395595379_pzrkjqvsr9nihts.jpeg",
        },
        {
            "title": "Совершенный код",
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
        **dict(context, template_name=template_name, **test_context)
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


@app.route('/scanner_data', methods=['POST'])
def scanner_data():
    form = request.form
    return ""


@app.route('/connect')
def get_current_user():
    client_ip = request.remote_addr
    terminal_uuid = uuid.uuid4()
    if(dbTerminalsFind(client_ip) is not None):
        return jsonify(terminal_uuid=dbTerminalsFindUUID(client_ip))
        dbTerminalsFind(client_ip)["uuid"]
    else:
        dbTerminalsInsert(client_ip, terminal_uuid)
        return jsonify(terminal_uuid=terminal_uuid)


def current_terminal_user(terminal):
    return "testUser"


def success_book_hand(terminal, book):
    pass


def success_book_return(terminal, book):
    pass


def user_book_operation(terminal, book):
    user = current_terminal_user(terminal)
    now = datetime.utcnow()
    if dbHandFind(user, book) is not None:
        dbHandsInsert(user, book)
        dbJournalInsert(user, book, "hand")
        success_book_hand(terminal, book)
    else:
        dbHandsRemove(user, book)
        dbJournalInsert(user, book, "return")
        success_book_return(terminal, book)


def main():
    logging.basicConfig(level=logging.DEBUG)
    config = load_config()
    app.run(host=config["host"], debug=True)


if __name__ == '__main__':
    main()
