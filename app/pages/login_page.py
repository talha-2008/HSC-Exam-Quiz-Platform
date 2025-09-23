import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Login", class_name="text-3xl font-bold text-gray-800 text-center"
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Username",
                            class_name="block text-sm font-medium text-gray-700",
                        ),
                        rx.el.input(
                            placeholder="Enter your username",
                            name="username",
                            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password",
                            class_name="block text-sm font-medium text-gray-700",
                        ),
                        rx.el.input(
                            placeholder="Enter your password",
                            name="password",
                            type="password",
                            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.div(
                            rx.icon(
                                "badge_alert", class_name="h-5 w-5 text-red-500 mr-2"
                            ),
                            rx.el.p(
                                AuthState.error_message,
                                class_name="text-sm text-red-600",
                            ),
                            class_name="flex items-center p-3 mb-4 bg-red-50 border border-red-200 rounded-lg",
                        ),
                    ),
                    rx.el.button(
                        "Login",
                        type="submit",
                        class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                    ),
                    on_submit=AuthState.login,
                ),
                rx.el.p(
                    "Don't have an account? ",
                    rx.el.a(
                        "Register here",
                        href="/register",
                        class_name="font-medium text-blue-600 hover:text-blue-500",
                    ),
                    class_name="mt-6 text-center text-sm text-gray-600",
                ),
                class_name="p-8 bg-white border border-gray-200 rounded-2xl shadow-md w-full max-w-md",
            ),
            class_name="flex flex-col items-center justify-center min-h-[calc(100vh-10rem)]",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )