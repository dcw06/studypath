"""
Entry point for the macOS app.
Starts Flask in a background thread, then opens a native WKWebView window.
"""

import sys
import threading
import time

import webview

# ── Resolve paths whether running as a script or a PyInstaller .app ───────────
import os

if getattr(sys, 'frozen', False):
    # Running inside a PyInstaller bundle
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)

# ── Configure Flask to find templates/static inside the bundle ────────────────
from flask import Flask
import app as flask_app_module

flask_app = flask_app_module.app
flask_app.template_folder = os.path.join(BASE_DIR, 'templates')
flask_app.static_folder   = os.path.join(BASE_DIR, 'static')

PORT = 5002


def _run_flask():
    flask_app.run(port=PORT, debug=False, use_reloader=False, threaded=True)


def main():
    # Start Flask in a daemon thread
    t = threading.Thread(target=_run_flask, daemon=True)
    t.start()

    # Give Flask a moment to bind
    time.sleep(1)

    # Open the native macOS window
    window = webview.create_window(
        title='Sign In',
        url=f'http://127.0.0.1:{PORT}/',
        width=560,
        height=820,
        resizable=True,
        min_size=(480, 600),
    )
    webview.start()


if __name__ == '__main__':
    main()
