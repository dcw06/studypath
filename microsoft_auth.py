#!/usr/bin/env python3
"""
Microsoft OAuth 2.0 authentication for the banking app.
Uses the Microsoft Identity Platform (personal + work/school accounts).
Register your app at: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps
Add http://127.0.0.1:8891/callback as a redirect URI (type: Web).
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

REDIRECT_URI     = "http://127.0.0.1:8891/callback"
MS_AUTH_URL      = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
MS_TOKEN_URL     = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
MS_USERINFO_URL  = "https://graph.microsoft.com/v1.0/me"

_auth_code     = None
_auth_error    = None
_auth_state    = None
_active_server = None
_cancelled     = False


class _ReuseAddrServer(HTTPServer):
    allow_reuse_address = True


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code, _auth_error
        params = parse_qs(urlparse(self.path).query)
        received_state = params.get("state", [None])[0]
        if received_state != _auth_state:
            _auth_error = "State mismatch — possible CSRF attack."
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h2>Sign-In Failed</h2><p>State mismatch.</p></body></html>")
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
            <h2 style="color:#00A4EF">Microsoft Sign-In Successful!</h2>
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
            <h2>Sign-In Failed</h2><p>{html.escape(_auth_error)}</p>
            </body></html>""".encode())
        threading.Thread(target=self.server.server_close, daemon=True).start()

    def log_message(self, format, *args):
        pass


def cancel_microsoft_auth():
    """Cancel an in-progress Microsoft login attempt."""
    global _cancelled, _active_server
    _cancelled = True
    if _active_server is not None:
        try:
            _active_server.server_close()
        except Exception:
            pass
        _active_server = None


def authenticate_with_microsoft(bank: Bank, create_if_missing: bool = True):
    """
    Authenticate via Microsoft OAuth.
    Returns (User, error, is_new).
    """
    global _auth_code, _auth_error, _auth_state, _active_server, _cancelled
    _auth_code  = None
    _auth_error = None
    _auth_state = secrets.token_urlsafe(16)
    _cancelled  = False

    if _active_server is not None:
        try:
            _active_server.server_close()
        except Exception:
            pass
        _active_server = None

    client_id     = config.MICROSOFT_CLIENT_ID
    client_secret = config.MICROSOFT_CLIENT_SECRET

    if not client_id or not client_secret:
        return None, (
            "Microsoft credentials are missing.\n"
            "Set MICROSOFT_CLIENT_ID and MICROSOFT_CLIENT_SECRET in your .env file.\n\n"
            "Setup steps:\n"
            "  1. Go to portal.azure.com → App registrations → New registration\n"
            "  2. Supported account types: Personal + work/school\n"
            f"  3. Add '{REDIRECT_URI}' as a redirect URI (Web)\n"
            "  4. Create a client secret under Certificates & secrets"
        ), False

    try:
        server = _ReuseAddrServer(("127.0.0.1", 8891), _CallbackHandler)
        _active_server = server
        threading.Thread(target=server.handle_request, daemon=True).start()

        params = {
            "client_id":     client_id,
            "response_type": "code",
            "redirect_uri":  REDIRECT_URI,
            "scope":         "openid profile email User.Read",
            "response_mode": "query",
            "state":         _auth_state,
        }
        webbrowser.open(f"{MS_AUTH_URL}?{urlencode(params)}")

        timeout, elapsed = 120, 0
        while _auth_code is None and _auth_error is None and elapsed < timeout and not _cancelled:
            time.sleep(0.5)
            elapsed += 0.5

        if _auth_error:
            return None, f"Microsoft sign-in was cancelled or denied: {_auth_error}", False
        if _auth_code is None:
            return None, "Microsoft login timed out. Please try again.", False

        # Exchange code for token
        resp = requests.post(MS_TOKEN_URL, data={
            "client_id":     client_id,
            "client_secret": client_secret,
            "code":          _auth_code,
            "redirect_uri":  REDIRECT_URI,
            "grant_type":    "authorization_code",
        }, timeout=30)
        token_data = resp.json()
        if "error" in token_data:
            raise Exception(f"{token_data['error']}: {token_data.get('error_description', '')}")
        access_token = token_data["access_token"]

        # Get user profile
        info = requests.get(MS_USERINFO_URL, headers={
            "Authorization": f"Bearer {access_token}"
        }, timeout=30).json()

        email     = info.get("mail") or info.get("userPrincipalName") or f"ms:{info.get('id', 'unknown')}"
        full_name = info.get("displayName", "")

        for user in bank.list_users():
            if user.username == email:
                if not user.display_name and full_name:
                    user.display_name = full_name
                    save_bank(bank)
                return user, None, False

        if not create_if_missing:
            return None, (
                "No account found for this Microsoft account.\n\n"
                "Please use 'Create Account' to register first."
            ), False

        new_user = bank.create_user(email, info.get("id", ""))
        new_user.display_name = full_name
        new_user.email_verified = True
        save_bank(bank)
        return new_user, None, True

    except Exception as e:
        return None, f"Error during Microsoft login: {e}", False
