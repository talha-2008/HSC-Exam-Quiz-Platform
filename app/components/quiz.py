import reflex as rx
from app.states.state import QuizState


def timer_display() -> rx.Component:
    return rx.el.div(
        rx.icon("timer", class_name="h-6 w-6 mr-2 text-red-500"),
        rx.el.p(
            QuizState.formatted_time_left,
            class_name="text-xl font-semibold text-red-500",
        ),
        class_name="flex items-center p-3 bg-red-50 border border-red-200 rounded-xl",
    )


def question_card() -> rx.Component:
    current_q = QuizState.current_questions[QuizState.current_question_index]
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                f"Question {QuizState.current_question_index + 1}/{QuizState.current_questions.length()}",
                class_name="text-sm font-medium text-gray-500",
            ),
            timer_display(),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.h3(
            current_q["question"], class_name="text-xl font-semibold text-gray-800 mb-6"
        ),
        rx.el.div(
            rx.foreach(
                current_q["options"],
                lambda option, index: rx.el.label(
                    rx.el.input(
                        type="radio",
                        name=f"q{QuizState.current_question_index}",
                        value=option,
                        on_change=lambda: QuizState.select_answer(
                            QuizState.current_question_index, option
                        ),
                        checked=QuizState.selected_answers.get(
                            QuizState.current_question_index, ""
                        )
                        == option,
                        class_name="sr-only peer",
                    ),
                    rx.el.div(
                        option,
                        class_name="w-full p-4 text-gray-600 bg-white border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 peer-checked:border-blue-500 peer-checked:bg-blue-50 peer-checked:text-blue-700 transition-all",
                    ),
                    class_name="w-full",
                ),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
        ),
        class_name="p-8 bg-white border border-gray-200 rounded-2xl shadow-md w-full max-w-3xl",
    )


def quiz_navigation_buttons() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("arrow-left", class_name="mr-2"),
            "Previous",
            on_click=QuizState.prev_question,
            disabled=QuizState.current_question_index == 0,
            class_name="flex items-center px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-xl hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all",
        ),
        rx.el.button(
            "Submit Quiz",
            on_click=QuizState.submit_quiz,
            class_name="px-8 py-3 bg-green-500 text-white font-semibold rounded-xl hover:bg-green-600 transition-all shadow-lg",
        ),
        rx.el.button(
            "Next",
            rx.icon("arrow-right", class_name="ml-2"),
            on_click=QuizState.next_question,
            disabled=QuizState.current_question_index
            == QuizState.current_questions.length() - 1,
            class_name="flex items-center px-6 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all",
        ),
        class_name="flex justify-between items-center mt-8 w-full max-w-3xl",
    )


def quiz_interface() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            f"{QuizState.current_subject} Quiz",
            class_name="text-3xl font-bold text-gray-800 mb-6",
        ),
        question_card(),
        quiz_navigation_buttons(),
        class_name="flex flex-col items-center justify-center min-h-[calc(100vh-10rem)] w-full",
    )