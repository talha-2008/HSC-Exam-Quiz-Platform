import reflex as rx
from app.components.navbar import navbar
from app.states.state import QuizState
from app.components.dashboard import performance_chart


def history_item(result, index: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            result["date"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            result["subject"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            f"{result['score']}/{result['total']}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            rx.el.span(
                f"{result['percentage']}%",
                class_name=rx.cond(
                    result["percentage"] >= 80,
                    "px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
                    rx.cond(
                        result["percentage"] >= 50,
                        "px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800",
                        "px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800",
                    ),
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        class_name="hover:bg-gray-50",
    )


def history_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            rx.el.h2(
                "Quiz History", class_name="text-3xl font-bold text-gray-800 mb-6"
            ),
            rx.cond(
                QuizState.total_quizzes_taken > 0,
                rx.el.div(
                    performance_chart(),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Date",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Subject",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Score",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Percentage",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(QuizState.quiz_history_list, history_item),
                                class_name="bg-white divide-y divide-gray-200",
                            ),
                            class_name="min-w-full divide-y divide-gray-200",
                        ),
                        class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg mt-8",
                    ),
                    class_name="mt-6",
                ),
                rx.el.div(
                    rx.icon("history", class_name="h-12 w-12 text-gray-400 mb-4"),
                    rx.el.p(
                        "No quiz history yet.",
                        class_name="text-lg font-medium text-gray-600",
                    ),
                    rx.el.p(
                        "Take a quiz to see your progress here!",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="text-center p-12 bg-white rounded-2xl border border-dashed",
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )