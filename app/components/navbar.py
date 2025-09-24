import reflex as rx
from app.states.state import QuizState
from app.states.auth_state import AuthState
from app.states.ui_state import UIState


def navbar() -> rx.Component:
    # Top-level container
    header_content = rx.el.div(
        # left: logo + title
        rx.el.div(
            rx.icon("book-open-check", class_name="h-8 w-8 text-blue-500"),
            rx.el.div(
                rx.el.h1(
                    "HSC Quiz App",
                    class_name="text-2xl font-bold text-gray-800 ml-2",
                ),
                rx.el.p(
                    "by talha",
                    class_name="text-sm text-gray-500 ml-2 mt-0.5",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center",
        ),

        # right: mobile button (visible on small) and desktop menu
        rx.el.div(
            # mobile hamburger (visible on small screens)
            rx.el.button(
                rx.icon("menu", class_name="h-6 w-6 text-gray-700"),
                on_click=UIState.toggle_menu,
                class_name="flex md:hidden items-center justify-center p-2 rounded-md",
            ),

            # desktop links (hidden on small)
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
            class_name="flex items-center space-x-2",
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16",
    )

    # mobile drawer (appears below header on small screens)
    mobile_drawer = rx.cond(
        UIState.menu_open,
        rx.el.div(
            rx.el.a(
                "Home",
                href="/",
                on_click=[UIState.toggle_menu, QuizState.go_home],
                class_name="block px-4 py-3 text-gray-800 hover:bg-gray-50 text-lg font-medium border-b border-gray-100",
            ),
            rx.el.a(
                "Subjects",
                href="/subjects",
                on_click=UIState.toggle_menu,
                class_name="block px-4 py-3 text-gray-800 hover:bg-gray-50 text-lg font-medium border-b border-gray-100",
            ),
            rx.el.a(
                "History",
                href="/history",
                on_click=UIState.toggle_menu,
                class_name="block px-4 py-3 text-gray-800 hover:bg-gray-50 text-lg font-medium border-b border-gray-100",
            ),
            rx.el.a(
                "About",
                href="/about",
                on_click=UIState.toggle_menu,
                class_name="block px-4 py-3 text-gray-800 hover:bg-gray-50 text-lg font-medium",
            ),
            # auth actions for mobile: show Logout when logged in, otherwise Login/Register
            rx.cond(
                AuthState.is_logged_in,
                rx.el.button(
                    "Logout",
                    on_click=[UIState.toggle_menu, AuthState.logout],
                    class_name="w-full text-left px-4 py-3 text-red-600 font-medium",
                ),
                rx.el.div(
                    rx.el.a(
                        "Login",
                        href="/login",
                        on_click=UIState.toggle_menu,
                        class_name="block px-4 py-3 text-gray-800 hover:bg-gray-50 text-lg font-medium border-t border-gray-100",
                    ),
                    rx.el.a(
                        "Register",
                        href="/register",
                        on_click=UIState.toggle_menu,
                        class_name="block mx-4 my-3 px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg text-center",
                    ),
                ),
            ),
            class_name="md:hidden absolute top-16 left-0 right-0 bg-white shadow-md z-40",
        ),
        None,
    )

    return rx.el.div(
        header_content,
        mobile_drawer,
        class_name="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50",
    )