import os
import sys

from zulip_gtk.ui import ZulipGtk
from zulip_gtk.zulip_client import ZulipClient


def main():
    zulip_email = os.environ.get("ZULIP_EMAIL") or ""
    zulip_key = os.environ.get("ZULIP_KEY") or ""
    zulip_url = os.environ.get("ZULIP_URL") or ""
    zulip_client = ZulipClient(zulip_email, zulip_key, zulip_url)

    app = ZulipGtk(zulip_client)
    exit_status = app.run(None)
    sys.exit(exit_status)


main()
