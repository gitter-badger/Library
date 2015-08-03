#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading, time, requests

def functionUser():
	devise = open("path")
	requests.post(url = "localhost:5000", data = {"type": "user", "data": devise.readline().strip("\2\3\r\n")})

def functionBook():
	devise = open("path")
	requests.post(url = "localhost:5000", data = {"type": "book", "data": devise.readline().strip("\2\3\r\n")})

threadUser = threading.Thread(target = functionUser)
threadBook = threading.Thread(target = functionBook)