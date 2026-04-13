#!/usr/bin/env python3
"""
Facebook OAuth 2.0 authentication for the banking app.
Requires a Facebook App with "Facebook Login" enabled and
http://localhost:8890/callback registered as a valid OAuth redirect URI.
Get credentials at: https://developers.facebook.com/apps
"""

import html
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode, parse_qs, urlparse

import requests

import config
from bank import Bank
from storage import save_bank

REDIRECT_URI    = "http://localhost:8890/callback"
FB_AUTH_URL     = "https://www.facebook.com/v18.0/dialog/oauth"
FB_TOKEN_URL    = "https://graph.facebook.com/v18.0/oauth/access_token"
FB_USERINFO_URL = "https://graph.facebook.com/me"

_auth_code     = None
_auth_error    = None
_auth_state    = None
_active_server = None
_cancelled     = False


class _ReuseAddrServer(HTTPServer):
    allow_reuse_address = True


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code, _auth_error, _active_server
        params = parse_qs(urlparse(self.path).query)
        received_state = params.get("state", [None])[0]
        if received_state != _auth_state:
            _auth_error = "State mismatch — possible CSRF attack."
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h2>Login Failed</h2><p>State mismatch.</p></body></html>")
            threading.Thread(target=self.server.server_close, daemon=True).start()
            return
        if "code" in params:
            _auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("""
            <html>
            <head><meta charset="utf-8"></head>
            <body style="text-align:center;margin-top:60px;font-family:Arial">
            <h2 style="color:#1877F2">Facebook Login Successful!</h2>
            <p>Closing in <span id="t">3</span> second(s)&hellip;</p>
            <script>
            var n=3;
            var iv=setInterval(function(){
                n--;
                document.getElementById('t').textContent=n;
                if(n<=0){clearInterval(iv);window.open('','_self','').close();}
            },1000);
            </script>
            </body></html>""".encode('utf-8'))
        else:
            _auth_error = params.get("error_description", ["Unknown error"])[0]
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"""
            <html><body style="text-align:center;margin-top:60px;font-family:Arial">
            <h2>Login Failed</h2><p>{html.escape(_auth_error)}</p>
            </body></html>""".encode())
        # Free the port immediately after receiving the callback
        threading.Thread(target=self.server.server_close, daemon=True).start()

    def log_message(self, format, *args):
        pass


def cancel_facebook_auth():
    """Cancel an in-progress Facebook login attempt."""
    global _cancelled, _active_server
    _cancelled = True
    if _active_server is not None:
        try:
            _active_server.server_close()
        except Exception:
            pass
        _active_server = None


def authenticate_with_facebook(bank: Bank, create_if_missing: bool = True):
    """
    Authenticate via Facebook OAuth.
    Returns (User, error, is_new).
    """
    global _auth_code, _auth_error, _auth_state, _active_server, _cancelled
    _auth_code  = None
    _auth_error = None
    _auth_state = secrets.token_urlsafe(16)
    _cancelled  = False

    # Close any previous server so the port is free
    if _active_server is not None:
        try:
            _active_server.server_close()
        except Exception:
            pass
        _active_server = None

    app_id     = config.FACEBOOK_APP_ID
    app_secret = config.FACEBOOK_APP_SECRET

    if not app_id or not app_secret:
        return None, (
            "Facebook credentials are missing.\n"
            "Set FACEBOOK_APP_ID and FACEBOOK_APP_SECRET in your .env file.\n"
            "Get them from: https://developers.facebook.com/apps\n\n"
            "In your app dashboard:\n"
            "  • Add 'Facebook Login' product\n"
            f"  • Add '{REDIRECT_URI}' as a Valid OAuth Redirect URI"
        ), False

    try:
        server = _ReuseAddrServer(("localhost", 8890), _CallbackHandler)
        _active_server = server
        threading.Thread(target=server.handle_request, daemon=True).start()

        params = {
            "client_id":     app_id,
            "redirect_uri":  REDIRECT_URI,
            "scope":         "email,public_profile",
            "response_type": "code",
            "state":         _auth_state,
        }
        webbrowser.open(f"{FB_AUTH_URL}?{urlencode(params)}")

        timeout, elapsed = 120, 0
        while _auth_code is None and _auth_error is None and elapsed < timeout and not _cancelled:
            time.sleep(0.5)
            elapsed += 0.5

        if _auth_error:
            return None, f"Facebook sign-in was cancelled or denied: {_auth_error}", False
        if _auth_code is None:
            return None, "Facebook login timed out. Please try again.", False

        # Exchange code for token
        resp = requests.get(FB_TOKEN_URL, params={
            "client_id":     app_id,
            "client_secret": app_secret,
            "redirect_uri":  REDIRECT_URI,
            "code":          _auth_code,
        }, timeout=30)
        data = resp.json()
        if "error" in data:
            raise Exception(data["error"].get("message", str(data["error"])))
        access_token = data["access_token"]

        # Get user info
        info = requests.get(FB_USERINFO_URL, params={
            "fields":       "id,name,email",
            "access_token": access_token,
        }, timeout=30).json()

        # Use email if available, else fall back to fb:<id>
        username  = info.get("email") or f"fb:{info['id']}"
        full_name = info.get("name", "")

        for user in bank.list_users():
            if user.username == username:
                if not user.display_name and full_name:
                    user.display_name = full_name
                    save_bank(bank)
                return user, None, False

        if not create_if_missing:
            return None, (
                "No account found for this Facebook account.\n\n"
                "Please use 'Create Account' to register first."
            ), False

        new_user = bank.create_user(username, info["id"])
        new_user.display_name = full_name
        new_user.email_verified = True  # Facebook identity already verified
        save_bank(bank)
        return new_user, None, True

    except Exception as e:
        return None, f"Error during Facebook login: {e}", False
