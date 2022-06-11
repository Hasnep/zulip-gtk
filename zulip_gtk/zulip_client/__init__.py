from typing import Dict, List, Optional, Union

import zulip

from zulip_gtk.zulip_client.messages import GetMessagesResponse
from zulip_gtk.zulip_client.streams import (
    GetStreamTopicsResponse,
    GetSubscriptionsResponse,
)


class ZulipClient:
    def __init__(
        self,
        email: str,
        api_key: str,
        site: str,
    ):
        self.client = zulip.Client(email=email, api_key=api_key, site=site)

    def get_narrow(
        self, stream: Optional[str] = None, topic: Optional[str] = None
    ) -> List[Dict[str, str]]:
        narrow: List[Dict[str, str]] = []
        if stream:
            narrow.append({"operator": "stream", "operand": stream})
        if topic:
            narrow.append({"operator": "topic", "operand": topic})
        return narrow

    def get_subscriptions(
        self, include_subscribers: bool = False
    ) -> GetSubscriptionsResponse:
        parameters = {"include_subscribers": include_subscribers}
        print(f"Getting subscriptions with parameters {parameters}.")
        response = self.client.get_subscriptions(parameters)
        return GetSubscriptionsResponse.parse_obj(response)

    def get_messages(
        self,
        anchor: Union[str, int],
        num_before: int,
        num_after: int,
        narrow: List[Dict[str, str]] = [],
        client_gravatar: bool = True,
        apply_markdown: bool = True,
    ) -> GetMessagesResponse:
        parameters = {
            "num_before": num_before,
            "num_after": num_after,
            "anchor": anchor,
            "narrow": narrow,
            "apply_markdown": apply_markdown,
        }
        print(f"Getting messages with parameters {parameters}.")
        response = self.client.get_messages(parameters)
        return GetMessagesResponse.parse_obj(response)

    def get_stream_topics(self, stream_id: int) -> GetStreamTopicsResponse:
        print(f"Getting stream topics for stream id {stream_id}")
        response = self.client.get_stream_topics(stream_id)
        return GetStreamTopicsResponse.parse_obj(response)
