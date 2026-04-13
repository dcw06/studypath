"""
Loads credentials from the .env file and exposes them as module-level constants.
"""

from dotenv import load_dotenv
import os

load_dotenv()

# Facebook
FACEBOOK_APP_ID     = os.getenv("FACEBOOK_APP_ID", "")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET", "")

# GitHub
GITHUB_CLIENT_ID     = os.getenv("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "")

# Microsoft
MICROSOFT_CLIENT_ID     = os.getenv("MICROSOFT_CLIENT_ID", "")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET", "")
