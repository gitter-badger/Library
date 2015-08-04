#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading, time, requests, configparser

config = configparser.ConfigParser()
config.read('config.cf')

def functionUser():
    device = open(config["Demon"]["userScanner"])
    requests.post(url = "http://localhost:5000/term", data = {"type": "user", "data": device.readline().strip("\2\3\r\n"), "id": "testTerminal"})

def functionBook():
    device = open(config["Demon"]["bookScanner"])
    requests.post(url = "http://localhost:5000/term", data = {"type": "book", "data": device.readline().strip("\2\3\r\n"), "id": "testTerminal"})

threadUser = threading.Thread(target = functionUser)
threadBook = threading.Thread(target = functionBook)