from datetime import datetime as DateTime

from zulip_gtk.ui.header_bar import RefreshButton
from zulip_gtk.ui.message import Message
from zulip_gtk.zulip_client import messages
from zulip_gtk.zulip_client.streams import SubscriptionResponse
from zulip_gtk.ui.stream import Stream
from zulip_gtk.ui.header_bar import HeaderBar


# Load Gtk
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gio


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


class MainPaned(Gtk.Paned):
    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_position(200)  # default width

        # Right
        self.main_stack = self.MainStack()
        self.set_end_child(self.main_stack)

        # Left
        self.sidebar = self.SideBar()
        self.sidebar.set_stack(self.main_stack)
        self.set_start_child(self.sidebar)

    class MainStack(Gtk.Stack):
        def __init__(self):
            super().__init__()
            self.set_transition_type(Gtk.StackTransitionType.SLIDE_RIGHT)

        def add_stream(self, stream_data: SubscriptionResponse):
            stream_widget = Stream(stream_data.name)
            self.add_titled(
                stream_widget,
                name=stream_data.name,
                title=stream_data.name,
            )

    class SideBar(Gtk.StackSidebar):
        def __init__(self):
            super().__init__()
