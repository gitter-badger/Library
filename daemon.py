#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import wx
import wx.html2
import requests
from threading import Thread
import ConfigParser


def load_config():
    config = ConfigParser.ConfigParser()
    config.read("config")
    return config


class MyBrowser(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize(wx.GetDisplaySize())


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
    if pack.user is not None and pack.book is None:
        pack.user = user
        return
    if pack == pack_none:
        pack.user = user
    else:
        pack.user = user
        send_scanner_data(pack.user, pack.book)
        pack = pack_none


def scan_book(device_file):
    global pack, pack_none
    book = scanner_read(device_file)
    if pack.book is not None and pack.user is None:
        pack.book = book
        return
    if pack == pack_none:
        pack.book = book
    else:
        pack.book = book
        send_scanner_data(pack.user, pack.book)
        pack = pack_none


def main():
    config = load_config()
    terminal_uuid = requests.get("http://localhost:5000/connect").json()["terminal_uuid"]
    thread_user = Thread(target=scan_user, args=config.get("Demon", "userScanner"))
    thread_book = Thread(target=scan_book, args=config.get("Demon", "bookScanner"))
    thread_book.start()
    thread_user.start()
    app = wx.App()
    dialog = MyBrowser(None, -1)
    dialog.browser.LoadURL(config.get("Demon", "url"))
    dialog.SetTitle("Библиотека Московского Химического Лицея")
    dialog.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
