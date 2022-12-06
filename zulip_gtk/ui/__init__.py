from typing import Any, Dict, List, Optional

import gi

from zulip_gtk.ui.async_worker import AsyncWorker
from zulip_gtk.ui.header_bar import HeaderBar
from zulip_gtk.ui.stream import Stream
from zulip_gtk.ui.window import Window
from zulip_gtk.zulip_client import GetSubscriptionsResponse, ZulipClient
from zulip_gtk.zulip_client.messages import MessageResponse

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, GLib, Gtk  # noqa: E402


class ZulipGtk(Gtk.Application):
    def __init__(self, zulip_client: ZulipClient):
        GLib.set_application_name("Zulip GTK")
        Gtk.Application.__init__(
            self,
            application_id="com.example.GtkApplication",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )

        self.zulip_client = zulip_client

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        self.window = Window(self)
        self.window.present()
        self.window.header_bar.refresh_button.connect(
            "clicked", self.do_refresh_button_clicked
        )

    def do_refresh_button_clicked(self, _refresh_button: HeaderBar.RefreshButton):
        def completion_callback(
            worker: AsyncWorker, result: Gio.AsyncResult, handler_data: Any
        ):
            subscriptions: GetSubscriptionsResponse = worker.return_value(result)
            main_stack = self.window.main_paned.main_stack
            for subscription in subscriptions.subscriptions:
                main_stack.add_stream(subscription)
                stream = main_stack.get_child_by_name(subscription.name)
                stream.connect("map", self.do_refresh_stream, subscription.name)

        AsyncWorker(
            main_callback=self.zulip_client.get_subscriptions,
            completion_callback=completion_callback,
        ).start()

    def do_refresh_stream(self, stream: Stream, stream_name: str):
        def main_callback():
            return self.zulip_client.get_messages(
                "newest",
                10,
                0,
                self.zulip_client.get_narrow(stream_name),
                apply_markdown=False,
            ).messages

        def completion_callback(
            worker: AsyncWorker, result: Gio.AsyncResult, handler_data: Any
        ):
            messages: Optional[List[MessageResponse]] = worker.return_value(result)

            if messages is None:
                return

            for message in messages:
                stream.add_message(message)

        AsyncWorker(
            main_callback=main_callback,
            completion_callback=completion_callback,
        ).start()
