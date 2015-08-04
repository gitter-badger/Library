#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import json
import requests
from threading import Thread


def scanner_read(device_file):
    with open(device_file) as device:
        return device.readline().strip("\2\3\r\n")


def send_scanner_data(user, book):
    """ Send scanned data to the server """
    requests.post(
        "http://localhost:5000/scanner_data",
        data={"user": user, "book": book, "id": terminal_uuid},
    )


pack_none = {
    "user": None,
    "book": None,
}


pack = pack_none


def scan_user(device_file):
    global pack, pack_none
    user = scanner_read(device_file)
    if(pack.user != None and pack.book == None):
        pack.user = user
        return
    if(pack == pack_none):
        pack.user = user
    else:
        pack.user = user
        send_scanner_data(pack.user, pack.book)
        pack = pack_none


def scan_book(device_file):
    global pack, pack_none
    book = scanner_read(device_file)
    if(pack.book != None and pack.user == None):
        pack.book = book
        return
    if(pack == pack_none):
        pack.book = book
    else:
        pack.book = book
        send_scanner_data(pack.user, pack.book)
        pack = pack_none


def main():
    config = configparser.ConfigParser()
    config.read('config.cf')

    if "uuid" not in config["Demon"]:
        config["Demon"]["uuid"] = (
            requests.get("http://localhost:5000/connect").json
            ["terminal_uuid"]
        )
        terminal_uuid = config["Demon"]["uuid"]

    thread_user = Thread(
        target=scan_user, args=(config["Demon"]["userScanner"],)
    )
    thread_book = Thread(
        target=scan_book, args=(config["Demon"]["bookScanner"],)
    )


if __name__ == '__main__':
    main()
