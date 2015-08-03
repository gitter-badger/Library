#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading, time, requests, configparser

config = configparser.ConfigParser()
config.read('config.cf')

def functionUser():
	devise = open(config["Demon"]["userScanner"])
	requests.post(url = "localhost:5000", data = {"type": "user", "data": devise.readline().strip("\2\3\r\n")})

def functionBook():
	devise = open(config["Demon"]["bookScanner"])
	requests.post(url = "localhost:5000", data = {"type": "book", "data": devise.readline().strip("\2\3\r\n")})

threadUser = threading.Thread(target = functionUser)
threadBook = threading.Thread(target = functionBook)