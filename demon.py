#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import threading
import time
import requests


config = configparser.ConfigParser()
config.read('config.cf')


class Scanner:
    def __init__(self, device_file):
        self.device_file = open(device_file)
        self.fd = None

    def __enter__(self):
        assert self.fd is None
        self.fd = open(self.device_file)

    def __leave__(self):
        self.fd.close()
        self.fd = None


def send_terminal_data(user, book):
    requests.post(
        "http://localhost:5000/term",
        data={"user": user, "book": book, "id": "testTerminal"},
    )

pack_none = {
	"user": None,
	"book": None,
}

pack = pack_none

def scan_user():
	global pack, pack_none
    with Scanner(config["Demon"]["userScanner"]) as scanner:
    	user = scanner.read().strip("\2\3\r\n")
    	if(pack.user != None and pack.book == None):
    		pack.user = user
    		return
    	if(pack == pack_none):
        	pack.user = user
        else:
        	pack.user = user
        	send_terminal_data(pack.user, pack.book)
        	pack = pack_none


def scan_book():
    global pack, pack_none
    with Scanner(config["Demon"]["bookScanner"]) as scanner:
    	book = scanner.read().strip("\2\3\r\n")
    	if(pack.book != None and pack.user == None):
    		pack.book = book
    		return
    	if(pack == pack_none):
        	pack.book = book
        else:
        	pack.book = book
        	send_terminal_data(pack.user, pack.book)
        	pack = pack_none


def main():
    threadUser = threading.Thread(target=scan_user)
    threadBook = threading.Thread(target=scan_book)


if __name__ == '__main__':
    main()
