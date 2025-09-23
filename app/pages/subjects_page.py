import reflex as rx
from app.components.navbar import navbar
from app.pages.index_page import subject_selection


def subjects_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            subject_selection(),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )