import reflex as rx
from app.pages.index_page import index
from app.pages.subjects_page import subjects_page
from app.pages.history_page import history_page
from app.pages.about_page import about_page
from app.pages.login_page import login_page
from app.pages.register_page import register_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(subjects_page, route="/subjects")
app.add_page(history_page, route="/history")
app.add_page(about_page, route="/about")
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")