#!/usr/bin/env python3
"""
GitHub OAuth authentication for the banking app.
Register your OAuth App at: https://github.com/settings/developers
Set the Authorization callback URL to: http://127.0.0.1:8892/callback
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

REDIRECT_URI       = "http://127.0.0.1:8892/callback"
GH_AUTH_URL        = "https://github.com/login/oauth/authorize"
GH_TOKEN_URL       = "https://github.com/login/oauth/access_token"
GH_USERINFO_URL    = "https://api.github.com/user"
GH_USER_EMAIL_URL  = "https://api.github.com/user/emails"

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
            <h2 style="color:#24292E">GitHub Login Successful!</h2>
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
        threading.Thread(target=self.server.server_close, daemon=True).start()

    def log_message(self, format, *args):
        pass


def cancel_github_auth():
    """Cancel an in-progress GitHub login attempt."""
    global _cancelled, _active_server
    _cancelled = True
    if _active_server is not None:
        try:
            _active_server.server_close()
        except Exception:
            pass
        _active_server = None


def authenticate_with_github(bank: Bank, create_if_missing: bool = True):
    """
    Authenticate via GitHub OAuth.
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

    client_id     = config.GITHUB_CLIENT_ID
    client_secret = config.GITHUB_CLIENT_SECRET

    if not client_id or not client_secret:
        return None, (
            "GitHub credentials are missing.\n"
            "Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in your .env file.\n\n"
            "Setup steps:\n"
            "  1. Go to github.com/settings/developers → OAuth Apps → New\n"
            "  2. Application name: FinWise\n"
            f"  3. Authorization callback URL: {REDIRECT_URI}"
        ), False

    try:
        server = _ReuseAddrServer(("127.0.0.1", 8892), _CallbackHandler)
        _active_server = server
        threading.Thread(target=server.handle_request, daemon=True).start()

        params = {
            "client_id":    client_id,
            "redirect_uri": REDIRECT_URI,
            "scope":        "read:user user:email",
            "state":        _auth_state,
        }
        webbrowser.open(f"{GH_AUTH_URL}?{urlencode(params)}")

        timeout, elapsed = 120, 0
        while _auth_code is None and _auth_error is None and elapsed < timeout and not _cancelled:
            time.sleep(0.5)
            elapsed += 0.5

        if _auth_error:
            return None, f"GitHub sign-in was cancelled or denied: {_auth_error}", False
        if _auth_code is None:
            return None, "GitHub login timed out. Please try again.", False

        # Exchange code for token
        resp = requests.post(GH_TOKEN_URL, data={
            "client_id":     client_id,
            "client_secret": client_secret,
            "code":          _auth_code,
            "redirect_uri":  REDIRECT_URI,
        }, headers={"Accept": "application/json"}, timeout=30)
        token_data = resp.json()
        if "error" in token_data:
            raise Exception(f"{token_data['error']}: {token_data.get('error_description', '')}")
        access_token = token_data["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        }

        info = requests.get(GH_USERINFO_URL, headers=headers, timeout=30).json()

        # GitHub may not expose email in /user — fetch from /user/emails
        email = info.get("email")
        if not email:
            emails = requests.get(GH_USER_EMAIL_URL, headers=headers, timeout=30).json()
            primary = next((e for e in emails if e.get("primary") and e.get("verified")), None)
            email = primary["email"] if primary else f"gh:{info['id']}"

        full_name = info.get("name", "") or info.get("login", "")

        for user in bank.list_users():
            if user.username == email:
                if not user.display_name and full_name:
                    user.display_name = full_name
                    save_bank(bank)
                return user, None, False

        if not create_if_missing:
            return None, (
                "No account found for this GitHub account.\n\n"
                "Please use 'Create Account' to register first."
            ), False

        new_user = bank.create_user(email, str(info["id"]))
        new_user.display_name = full_name
        new_user.email_verified = True
        save_bank(bank)
        return new_user, None, True

    except Exception as e:
        return None, f"Error during GitHub login: {e}", False
