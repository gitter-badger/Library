#!/bin/bash

LIB_WX_WEBVIEW=/usr/lib/x86_64-linux-gnu/libwx_gtk2u_webview-3.0.so.0

if [ ! -f $LIB_WX_WEBVIEW ]; then
    echo 'Install package libwxgtk-webview3.0-0'
    exit 1
fi

export LD_PRELOAD=$LIB_WX_WEBVIEW
./daemon.py
