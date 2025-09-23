import reflex as rx
from app.states.state import QuizState


def dashboard_card(title: str, value: rx.Var, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-8 w-8 text-{color}-500"),
            class_name="p-3 bg-white rounded-full",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-3xl font-bold text-gray-800"),
            class_name="ml-4",
        ),
        class_name=f"flex items-center p-6 bg-{color}-50 border border-{color}-100 rounded-2xl shadow-sm hover:shadow-lg hover:scale-105 transition-all duration-300",
    )


def performance_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Performance Trend", class_name="text-lg font-semibold text-gray-700 mb-4"
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", class_name="opacity-50"),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "#FFFFFF",
                    "border": "1px solid #E5E7EB",
                    "borderRadius": "0.75rem",
                }
            ),
            rx.recharts.x_axis(data_key="date", class_name="text-xs"),
            rx.recharts.y_axis(domain=[0, 100], class_name="text-xs"),
            rx.recharts.legend(),
            rx.recharts.line(
                data_key="score",
                stroke="#3b82f6",
                stroke_width=2,
                name="Score (%)",
                dot={"r": 4, "fill": "#3b82f6"},
            ),
            data=QuizState.quiz_history_for_chart,
            height=300,
            class_name="font-sans",
        ),
        class_name="p-6 bg-white border border-gray-200 rounded-2xl shadow-sm mt-8",
    )


def dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Dashboard", class_name="text-3xl font-bold text-gray-800 mb-6"),
        rx.el.div(
            dashboard_card(
                "Total Quizzes", QuizState.total_quizzes_taken, "clipboard-list", "blue"
            ),
            dashboard_card(
                "Best Score", QuizState.best_score.to_string() + " %", "trophy", "green"
            ),
            dashboard_card(
                "Average Score",
                QuizState.average_percentage.to_string() + " %",
                "bar-chart-2",
                "yellow",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
        ),
        performance_chart(),
        class_name="mt-8",
    )