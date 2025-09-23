import reflex as rx
from app.components.navbar import navbar


def about_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "About HSC Quiz App",
                    class_name="text-4xl font-extrabold text-gray-900 tracking-tight",
                ),
                rx.el.p(
                    "This application is designed to help students prepare for their Higher Secondary Certificate (HSC) exams.",
                    class_name="mt-4 text-lg text-gray-600",
                ),
                rx.el.p(
                    "Select subjects, take timed quizzes, and track your performance with detailed analytics. Our goal is to provide a modern, user-friendly, and effective learning tool.",
                    class_name="mt-2 text-lg text-gray-600",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Features:",
                        class_name="text-2xl font-bold text-gray-800 mt-10 mb-4",
                    ),
                    rx.el.ul(
                        rx.el.li(
                            "📚 Wide range of subjects including Bangla, Physics, Chemistry, Math, and Biology."
                        ),
                        rx.el.li("⏱️ Timed quizzes to simulate exam conditions."),
                        rx.el.li("📊 Instant results and performance analytics."),
                        rx.el.li(
                            "📈 Progress tracking with historical data and charts."
                        ),
                        rx.el.li("📱 Responsive design for learning on any device."),
                        class_name="list-disc list-inside space-y-2 text-gray-600",
                    ),
                    class_name="mt-6",
                ),
                class_name="max-w-3xl mx-auto py-16 px-4 sm:py-24 sm:px-6 lg:px-8 text-center",
            ),
            class_name="bg-white",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )