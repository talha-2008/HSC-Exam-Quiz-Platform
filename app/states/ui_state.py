import reflex as rx


class UIState(rx.State):
    menu_open: bool = False

    @rx.event
    def toggle_menu(self):
        self.menu_open = not self.menu_open
