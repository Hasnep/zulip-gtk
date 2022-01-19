from zulip_gtk.zulip_client.streams import SubscriptionResponse
from zulip_gtk.ui.stream import Stream


# Load Gtk
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


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
