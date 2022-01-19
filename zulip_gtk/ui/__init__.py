from zulip_gtk.ui.window import Window
from zulip_gtk.zulip_client import ZulipClient
from zulip_gtk.ui.header_bar import RefreshButton
from zulip_gtk.ui.stream import Stream

# Load Gtk
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gio, Pango


class ZulipGtk(Gtk.Application):
    def __init__(self, zulip_client: ZulipClient):
        GLib.set_application_name("Zulip GTK")
        Gtk.Application.__init__(self, application_id="com.example.GtkApplication")

        self.zulip_client = zulip_client

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        self.window = Window(self)
        self.window.present()
        self.window.header_bar.refresh_button.connect(
            "clicked", self.do_refresh_button_clicked
        )

    def do_refresh_button_clicked(self, _refresh_button: RefreshButton):
        subscriptions = self.zulip_client.get_subscriptions()
        main_stack = self.window.main_paned.main_stack
        for subscription in subscriptions.subscriptions:
            main_stack.add_stream(subscription)
            stream = main_stack.get_child_by_name(subscription.name)
            stream.connect("map", self.do_refresh_stream, subscription.name)

    # def do_stream_map(self,stream:Stream,stream_name:str):

    def do_refresh_stream(self, stream: Stream, stream_name: str):
        response = self.zulip_client.get_messages(
            "newest",
            10,
            0,
            self.zulip_client.get_narrow(stream_name),
            apply_markdown=False,
        )
        messages = response.messages
        if messages is None:
            return

        for message in messages:
            stream.add_message(message)