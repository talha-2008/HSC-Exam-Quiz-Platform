import reflex as rx
from app.components.navbar import navbar
from app.components.dashboard import dashboard
from app.components.quiz import quiz_interface
from app.components.results import results_page
from app.states.state import QuizState


def subject_card(subject: str) -> rx.Component:
    colors = {
        "Bangla": "blue",
        "Physics": "purple",
        "Chemistry": "green",
        "Math": "orange",
        "Biology": "teal",
    }
    color = colors.get(subject, "gray")
    return rx.el.div(
        rx.el.h3(subject, class_name="text-xl font-bold text-white"),
        rx.el.p(
            "Ready to test your knowledge?", class_name="text-sm text-white/80 mt-2"
        ),
        rx.el.button(
            "Start Quiz",
            on_click=lambda: QuizState.start_quiz(subject),
            class_name=f"mt-4 px-4 py-2 bg-white text-{color}-600 font-semibold rounded-lg hover:bg-gray-100 transition-all",
        ),
        class_name=f"p-6 bg-gradient-to-br from-{color}-500 to-{color}-600 rounded-2xl shadow-lg hover:shadow-xl hover:-translate-y-1 transform transition-all duration-300 cursor-pointer",
    )


def subject_selection() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Select a Subject",
            class_name="text-3xl font-bold text-gray-800 mb-8 text-center",
        ),
        rx.el.div(
            rx.foreach(QuizState.subjects, subject_card),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8",
        ),
        class_name="w-full",
    )


def main_content() -> rx.Component:
    return rx.cond(
        QuizState.quiz_in_progress,
        quiz_interface(),
        rx.cond(
            QuizState.quiz_submitted,
            results_page(),
            rx.el.div(dashboard(), subject_selection(), class_name="space-y-12"),
        ),
    )


def index() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            main_content(), class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
        ),
        on_mount=QuizState.check_login,
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )