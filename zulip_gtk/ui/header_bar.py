import gi

# Load Gtk
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class HeaderBar(Gtk.HeaderBar):
    class RefreshButton(Gtk.Button):
        def __init__(self):
            super().__init__()
            self.set_icon_name("view-refresh")

    def __init__(self):
        super().__init__()
        self.refresh_button = self.RefreshButton()
        self.pack_start(self.refresh_button)
