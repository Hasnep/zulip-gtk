# Load Gtk
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class HeaderBar(Gtk.HeaderBar):
    def __init__(self):
        super().__init__()
        self.refresh_button = self.RefreshButton()
        self.pack_start(self.refresh_button)

    class RefreshButton(Gtk.Button):
        def __init__(self):
            super().__init__()
            self.set_icon_name("view-refresh")
