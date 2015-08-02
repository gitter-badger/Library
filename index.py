#!/usr/bin/env python3'
from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route("/")
def index():
	return redirect("/login")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/reg")
def reg():
	return render_template("reg.html")

app.run(host="::", port=5000, debug=True)