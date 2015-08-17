#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import wx
import wx.html2
from six.moves import configparser
import json
import requests
from threading import Thread


class MyBrowser(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize(wx.GetDisplaySize())



def load_config():
    config = configparser.ConfigParser()
    config.read('../..config')
    return config.options("Demon")


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
    if(pack.user is not None and pack.book is None):
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
    if(pack.book is not None and pack.user is None):
        pack.book = book
        return
    if(pack == pack_none):
        pack.book = book
    else:
        pack.book = book
        send_scanner_data(pack.user, pack.book)
        pack = pack_none


def main():
    config = load_config()

    if config.get("uuid") == "uuid":
        config.set("uuid", (requests.get("http://localhost:5000/connect").json
            ["terminal_uuid"]))
        terminal_uuid = config.get("uuid")

    thread_user = Thread(target=scan_user, args=(config["userScanner"],))
    thread_book = Thread(target=scan_book, args=(config["bookScanner"],))
    app = wx.App()
    dialog = MyBrowser(None, -1)
    dialog.browser.LoadURL("http://localhost:5000/")
    dialog.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
