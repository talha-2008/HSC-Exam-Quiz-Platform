import reflex as rx
from app.states.state import QuizState, WrongAnswer
from app.components.dashboard import performance_chart


def result_summary_card(
    title: str, value: str | rx.Var, icon: str, color: str
) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name=f"h-6 w-6 text-{color}-600"),
        rx.el.p(title, class_name="text-sm font-medium text-gray-500 ml-3"),
        rx.el.p(value, class_name="text-lg font-bold text-gray-800 ml-auto"),
        class_name=f"flex items-center p-4 bg-{color}-100 border border-{color}-200 rounded-xl",
    )


def result_pie_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Answer Breakdown", class_name="text-lg font-semibold text-gray-700 mb-4"
        ),
        rx.recharts.pie_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.pie(
                data=QuizState.result_pie_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                outer_radius=80,
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
        class_name="p-6 bg-white border border-gray-200 rounded-2xl shadow-sm",
    )


def wrong_answer_card(item: WrongAnswer) -> rx.Component:
    return rx.el.div(
        rx.el.p(item["question"], class_name="font-semibold text-gray-800 mb-3"),
        rx.el.div(
            rx.foreach(
                item["options"],
                lambda option: rx.el.div(
                    option,
                    class_name=rx.cond(
                        option == item["correct"],
                        "p-3 rounded-lg bg-green-100 text-green-800 border border-green-200",
                        rx.cond(
                            option == item["selected"],
                            "p-3 rounded-lg bg-red-100 text-red-800 border border-red-200",
                            "p-3 rounded-lg bg-gray-50 text-gray-700 border border-gray-200",
                        ),
                    ),
                ),
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 gap-2",
        ),
        class_name="p-4 bg-white border border-gray-200 rounded-xl mt-4",
    )


def results_page() -> rx.Component:
    return rx.cond(
        QuizState.has_last_result,
        rx.el.div(
            rx.el.h2("Quiz Result", class_name="text-3xl font-bold text-gray-800 mb-2"),
            rx.el.p(
                QuizState.last_result_subject,
                class_name="text-lg text-gray-600 mb-6",
            ),
            rx.el.div(
                result_summary_card(
                    "Score",
                    QuizState.last_result_score_text,
                    "check_check",
                    "green",
                ),
                result_summary_card(
                    "Percentage",
                    QuizState.last_result_percentage_text,
                    "percent",
                    "blue",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8",
            ),
            rx.el.div(
                result_pie_chart(),
                performance_chart(),
                class_name="grid md:grid-cols-2 gap-8 mb-8",
            ),
            rx.el.h3(
                "Review Wrong Answers",
                class_name="text-2xl font-bold text-gray-800 mb-4",
            ),
            rx.cond(
                QuizState.last_result_wrong_count > 0,
                rx.el.div(
                    rx.foreach(
                        QuizState.last_result_wrong_answers, wrong_answer_card
                    ),
                    class_name="space-y-4",
                ),
                rx.el.div(
                    rx.icon("party-popper", class_name="h-12 w-12 text-green-500 mb-4"),
                    rx.el.p(
                        "Congratulations! No wrong answers.",
                        class_name="text-lg font-semibold text-gray-700",
                    ),
                    class_name="flex flex-col items-center justify-center p-8 bg-green-50 border border-green-200 rounded-2xl",
                ),
            ),
            rx.el.div(
                rx.el.a(
                    "Back to Home",
                    href="/",
                    on_click=QuizState.go_home,
                    class_name="px-8 py-3 bg-blue-500 text-white font-semibold rounded-xl hover:bg-blue-600 transition-all",
                ),
                class_name="mt-8 flex justify-center",
            ),
            class_name="max-w-4xl mx-auto py-8",
        ),
        rx.el.div(
            rx.el.p("No results to display. Please complete a quiz first."),
            class_name="text-center text-gray-500",
        ),
    )