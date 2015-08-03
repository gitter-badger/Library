#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading, time

def userToServer(data):
	pass

def userToServer(data):
	pass

def functionUser():
	devise = open("path")
	data = devise.readline().strip("\2\3\r\n")
	userToServer(data)

def functionBook():
	devise = open("path")
	data = devise.readline().strip("\2\3\r\n")
	bookToServer(data)

threadUser = threading.Thread(target = functionUser)
threadBook = threading.Thread(target = functionBook)