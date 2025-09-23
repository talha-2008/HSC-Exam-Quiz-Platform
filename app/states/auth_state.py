import reflex as rx
import json
import logging
from typing import TypedDict


class User(TypedDict):
    username: str
    password_hash: str
    quiz_history: list


class AuthState(rx.State):
    users_json: str = rx.LocalStorage("{}", name="users")
    logged_in_user: str = rx.LocalStorage("", name="logged_in_user")
    error_message: str = ""
    success_message: str = ""

    @rx.var
    def users(self) -> dict[str, User]:
        try:
            return json.loads(self.users_json)
        except json.JSONDecodeError:
            logging.exception("Error decoding users_json")
            return {}

    @rx.var
    def is_logged_in(self) -> bool:
        return self.logged_in_user != ""

    @rx.var
    def current_user_data(self) -> User | None:
        if self.is_logged_in:
            return self.users.get(self.logged_in_user)
        return None

    def _save_users(self, users_data: dict[str, User]):
        self.users_json = json.dumps(users_data)

    def register(self, form_data: dict):
        self.error_message = ""
        self.success_message = ""
        username = form_data.get("username")
        password = form_data.get("password")
        if not username or not password:
            self.error_message = "Username and password are required."
            return
        current_users = self.users
        if username in current_users:
            self.error_message = "Username already exists."
            return
        current_users[username] = {
            "username": username,
            "password_hash": password,
            "quiz_history": [],
        }
        self._save_users(current_users)
        self.success_message = "Registration successful! Please log in."
        return rx.redirect("/login")

    def login(self, form_data: dict):
        self.error_message = ""
        self.success_message = ""
        username = form_data.get("username")
        password = form_data.get("password")
        user = self.users.get(username)
        if user and user["password_hash"] == password:
            self.logged_in_user = username
            return rx.redirect("/")
        else:
            self.error_message = "Invalid username or password."

    def logout(self):
        self.logged_in_user = ""
        return rx.redirect("/login")