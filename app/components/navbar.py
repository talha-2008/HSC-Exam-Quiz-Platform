import reflex as rx
from app.states.state import QuizState
from app.states.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("book-open-check", class_name="h-8 w-8 text-blue-500"),
                rx.el.h1(
                    "HSC Quiz App", class_name="text-2xl font-bold text-gray-800 ml-2"
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.a(
                    "Home",
                    href="/",
                    on_click=QuizState.go_home,
                    class_name="text-gray-600 hover:text-blue-500 font-medium px-3 py-2 rounded-md",
                ),
                rx.el.a(
                    "Subjects",
                    href="/subjects",
                    class_name="text-gray-600 hover:text-blue-500 font-medium px-3 py-2 rounded-md",
                ),
                rx.el.a(
                    "Quiz History",
                    href="/history",
                    class_name="text-gray-600 hover:text-blue-500 font-medium px-3 py-2 rounded-md",
                ),
                rx.el.a(
                    "About",
                    href="/about",
                    class_name="text-gray-600 hover:text-blue-500 font-medium px-3 py-2 rounded-md",
                ),
                rx.cond(
                    AuthState.is_logged_in,
                    rx.el.button(
                        "Logout",
                        on_click=AuthState.logout,
                        class_name="text-red-500 hover:text-red-700 font-medium px-3 py-2 rounded-md",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Login",
                            href="/login",
                            class_name="text-gray-600 hover:text-blue-500 font-medium px-3 py-2 rounded-md",
                        ),
                        rx.el.a(
                            "Register",
                            href="/register",
                            class_name="ml-2 px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 transition-all",
                        ),
                    ),
                ),
                class_name="hidden md:flex items-center space-x-2",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16",
        ),
        class_name="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50",
    )