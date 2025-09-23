import reflex as rx
import json
import logging
import threading
import os
import bcrypt
from typing import TypedDict


class User(TypedDict):
    username: str
    password_hash: str
    quiz_history: list


# module-level shared resources (don't attach non-picklable objects to State)
USERS_FILE = os.path.join(os.getcwd(), "data", "users.json")
USERS_FILE_LOCK = threading.Lock()


class AuthState(rx.State):
    # keep logged_in_user as client LocalStorage so the client remembers its session
    logged_in_user: str = rx.LocalStorage("", name="logged_in_user")
    error_message: str = ""
    success_message: str = ""

    @rx.var
    def users(self) -> dict[str, User]:
        # Read the shared users JSON file. If missing, create an empty file.
        try:
            os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
            if not os.path.exists(USERS_FILE):
                with open(USERS_FILE, "w", encoding="utf-8") as f:
                    json.dump({}, f)
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            logging.exception("Error reading users file")
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
        # Write to shared users file with a lock to avoid concurrent writes
        try:
            with USERS_FILE_LOCK:
                os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
                with open(USERS_FILE, "w", encoding="utf-8") as f:
                    json.dump(users_data, f)
        except Exception:
            logging.exception("Error saving users file")


    @rx.event
    def register(self, form_data: dict):
        self.error_message = ""
        self.success_message = ""
        username = form_data.get("username", "")
        password = form_data.get("password", "")
        if not username or not password:
            self.error_message = "Username and password are required."
            return
        current_users = self.users
        if username in current_users:
            self.error_message = "Username already exists."
            return
        # hash the password before saving
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        current_users[username] = {
            "username": username,
            "password_hash": hashed,
            "quiz_history": [],
        }
        self._save_users(current_users)
        self.success_message = "Registration successful! Please log in."
        return rx.redirect("/login")

    @rx.event
    def login(self, form_data: dict):
        self.error_message = ""
        self.success_message = ""
        username = form_data.get("username", "")
        password = form_data.get("password", "")
        user = self.users.get(username)
        if user:
            stored_hash = user.get("password_hash", "")
            # If the stored value looks like a bcrypt hash (starts with $2), verify with bcrypt.
            # Otherwise treat it as a legacy plaintext password: compare directly and migrate to bcrypt.
            try:
                if isinstance(stored_hash, str) and stored_hash.startswith("$2"):
                    # Normal bcrypt-stored password
                    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                        self.logged_in_user = username
                        from app.states.state import QuizState

                        return [rx.redirect("/"), QuizState.go_home]
                    else:
                        self.error_message = "Invalid username or password."
                        return
                else:
                    # Legacy plaintext password (or empty). Compare directly and migrate to bcrypt on success.
                    if password == stored_hash:
                        # Re-hash password and persist
                        try:
                            new_hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                            users_copy = self.users
                            users_copy[username]["password_hash"] = new_hashed
                            self._save_users(users_copy)
                        except Exception:
                            logging.exception("Error migrating plaintext password to bcrypt")
                        self.logged_in_user = username
                        from app.states.state import QuizState

                        return [rx.redirect("/"), QuizState.go_home]
                    else:
                        self.error_message = "Invalid username or password."
                        return
            except ValueError:
                # bcrypt can raise ValueError for invalid salt formats; log and fall back to safe message
                logging.exception("Error verifying password: invalid salt")
                self.error_message = "Invalid username or password."
                return
            except Exception:
                logging.exception("Error verifying password")
                self.error_message = "Invalid username or password."
                return
        else:
            self.error_message = "Invalid username or password."
            return

    @rx.event
    def logout(self):
        self.logged_in_user = ""
        return rx.redirect("/login")