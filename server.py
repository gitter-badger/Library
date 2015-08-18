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
    config.read('config')
    return config['Server']


def open_db():
    return pymongo.MongoClient().digital_library

db = open_db()


def db_terminal_add(client_ip, terminal_uuid):
    global db
    db.terminals.insert({"ip": client_ip, "uuid": str(terminal_uuid)})


def db_terminal_get(client_ip):
    global db
    return db.terminals.find_one({'ip': client_ip})


def db_terminal_get_uuid(client_ip):
    return db_terminal_get(client_ip)["uuid"]


def db_hand_add(user, book):
    global db
    now = datetime.utcnow()
    db.hands.insert({
        "user": user,
        "book": book,
        "datetime": now,
    })


def db_hand_get(user, book):
    global db
    return db.hands.find_one({'user': user, 'book': book})


def db_hand_exists(user, book):
    return db_hand_get(user, book) is not None


def db_hand_delete(user, book):
    global db
    db.hands.remove({"user": user, "book": book})


def db_handlog_add(user, book, event):
    global db
    assert event in {'take', 'return'}
    now = datetime.utcnow()
    db.handlog.insert({
        "user": user,
        "book": book,
        "datetime": now,
        "event": event,
    })


def render_template(template_name, **context):
    test_books = [
        {
            "title": "Что такое математика?",
            "author": "Р. Курант, Г. Роббинс",
            "id": "curant",
        },
        {
            "title": "Сборник задач по алгебре",
            "author": "М.Л. Галицкий, А.М. Гольдман, Л.И. Звавич",
            "id": "gal",
        },
        {
            "title": "Алгоритмы: построение и анализ",
            "author": "К. Штайн, Р. Линн Ривест, Т. Кормен, Ч. Эрик Лейзерсон",
            "id": "cormen",
        },
        {
            "title": "Совершенный код",
            "author": "С. Макконнелл",
            "id": "codecompl",
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


@app.route('/connect')
def get_current_user():
    client_ip = request.remote_addr
    terminal = db_terminal_get(client_ip)
    if terminal is not None:
        return jsonify(terminal_uuid=terminal['uuid'])
    else:
        terminal_uuid = uuid.uuid4()
        db_terminal_add(client_ip, terminal_uuid)
        return jsonify(terminal_uuid=terminal_uuid)


@app.route('/api/book/action', methods=['POST'])
def api_book_action():
    form = request.form
    user, book = form["user"], form["book"]
    if db_hand_exists(user, book):
        db_hand_delete(user, book)
        db_handlog_add(user, book, "return")
        action = "return"
    else:
        db_hand_add(user, book)
        db_handlog_add(user, book, "take")
        action = "take"
    return jsonify(action=action, book=book)


def main():
    logging.basicConfig(level=logging.DEBUG)
    config = load_config()
    app.run(host=config["host"], debug=True)


if __name__ == '__main__':
    main()
