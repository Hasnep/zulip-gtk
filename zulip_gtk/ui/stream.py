from zulip_gtk.ui.message import Message

# Load Gtk
import gi

from zulip_gtk.zulip_client.messages import MessageResponse

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class Stream(Gtk.ScrolledWindow):
    def __init__(self, stream_name: str):
        super().__init__()
        self.set_max_content_width(200)

        self.message_list = self.StreamMessageList(stream_name)
        self.set_child(self.message_list)

    def add_message(self, message: MessageResponse):
        self.message_list.add_message(message)

    class StreamMessageList(Gtk.ListBox):
        def __init__(self, stream_name: str):
            super().__init__()
            self.set_hexpand(False)

            self.stream_name = stream_name

        def add_message(self, message_data: MessageResponse):
            message = Message(message_data)
            self.append(message)
