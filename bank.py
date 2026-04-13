"""
Core domain models for the banking app.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class User:
    username: str
    password_hash: str
    display_name: str = ""
    email_verified: bool = False


@dataclass
class Bank:
    _users: List[User] = field(default_factory=list)

    def list_users(self) -> List[User]:
        return list(self._users)

    def create_user(self, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)
        self._users.append(user)
        return user

    def get_user(self, username: str) -> Optional[User]:
        return next((u for u in self._users if u.username == username), None)
