from zulip_gtk.ui.header_bar import HeaderBar
from zulip_gtk.ui.main_paned import MainPaned


# Load Gtk
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class Window(Gtk.ApplicationWindow):
    __gtype_name__ = "ListViewExampleWindow"

    def __init__(self, app: Gtk.Application):
        Gtk.ApplicationWindow.__init__(self, application=app)
        self.set_default_size(980, 640)
        self.set_size_request(-1, 300)
        # self.set_position(Gtk.WindowPosition.CENTER)

        # Top
        self.header_bar = HeaderBar()
        self.set_titlebar(self.header_bar)

        # Main
        self.main_paned = MainPaned()
        self.set_child(self.main_paned)
