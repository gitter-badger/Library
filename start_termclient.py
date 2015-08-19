#!/usr/bin/env python3

import os
import sys
import subprocess

WX_WEBVIEW_LIB_NAMES = [
    '/usr/lib/x86_64-linux-gnu/libwx_gtk2u_webview-3.0.so.0',
    '/usr/lib/i386-linux-gnu/libwx_gtk2u_webview-3.0.so.0',
]

for lib_name in WX_WEBVIEW_LIB_NAMES:
    if os.path.exists(lib_name):
        WX_WEBVIEW_LIB = lib_name
        break
else:
    print('Install package libwxgtk-webview3.0-0', file=sys.stderr)
    sys.exit(1)

os.environ['LD_PRELOAD'] = WX_WEBVIEW_LIB
subprocess.check_call('./client.py')
