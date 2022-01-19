from datetime import datetime as DateTime

from zulip_gtk.zulip_client.messages import MessageResponse

# Load Gtk
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

AVATAR_SIZE = 64


class Message(Gtk.Box):
    def __init__(self, message_data: MessageResponse):
        super().__init__()
        self.set_orientation(Gtk.Orientation.HORIZONTAL)

        # Left
        self.avatar = self.Avatar()
        self.append(self.avatar)

        # Middle
        self.content_box = self.MessageContent(message_data)
        self.append(self.content_box)

        # Right
        self.timestamp_label = self.MessageTimestamp(message_data)
        self.append(self.timestamp_label)

    class Avatar(Gtk.Image):
        def __init__(self):
            super().__init__()
            self.set_from_icon_name("dialog-information")
            self.set_size_request(AVATAR_SIZE, AVATAR_SIZE)
            self.set_valign(Gtk.Align.START)

    class MessageContent(Gtk.Box):
        def __init__(self, message_data: MessageResponse):
            super().__init__()
            self.set_orientation(Gtk.Orientation.VERTICAL)
            self.set_hexpand(True)

            # Top
            self.sender_label = self.MessageSender(message_data)
            self.append(self.sender_label)

            # Bottom
            self.message_text = self.MessageText(message_data)
            self.append(self.message_text)

        class MessageSender(Gtk.Label):
            def __init__(self, message_data: MessageResponse):
                super().__init__()
                self.set_halign(Gtk.Align.START)
                self.set_text(message_data.sender_full_name)
                # self.set_attributes()

        class MessageText(Gtk.Label):
            def __init__(self, message_data: MessageResponse):
                super().__init__()
                self.set_halign(Gtk.Align.START)
                self.set_wrap(True)
                self.set_text(message_data.content)

    class MessageTimestamp(Gtk.Label):
        def __init__(self, message_data: MessageResponse):
            super().__init__()
            self.set_text(
                DateTime.fromtimestamp(message_data.timestamp).strftime(r"%Y-%m-%d")
            )
            self.set_halign(Gtk.Align.END)
            self.set_valign(Gtk.Align.START)
