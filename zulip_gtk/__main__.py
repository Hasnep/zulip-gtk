from zulip_gtk.zulip_client import ZulipClient
from zulip_gtk.ui import ZulipGtk

import os
import sys


def main():
    zulip_email = os.environ.get("ZULIP_EMAIL") or ""
    zulip_key = os.environ.get("ZULIP_KEY") or ""
    zulip_url = os.environ.get("ZULIP_URL") or ""
    zulip_client = ZulipClient(zulip_email, zulip_key, zulip_url)
    # messages = zulip_client.get_messages("newest", 10, 0)

    app = ZulipGtk(zulip_client)
    exit_status = app.run(None)
    sys.exit(exit_status)


main()
