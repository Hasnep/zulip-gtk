from pydantic import BaseModel, Field
from typing import List, Optional, Union


class SubscriptionResponse(BaseModel):
    stream_id: int
    name: str
    description: str
    rendered_description: str
    date_created: int
    invite_only: bool
    # subscribers: List[int]
    desktop_notifications: Optional[bool]
    email_notifications: Optional[bool]
    wildcard_mentions_notify: Optional[bool]
    push_notifications: Optional[bool]
    audible_notifications: Optional[bool]
    pin_to_top: bool
    email_address: str
    is_muted: bool
    is_announcement_only: bool
    is_web_public: bool
    role: int
    color: str
    stream_post_policy: int
    message_retention_days: Optional[int]
    history_public_to_subscribers: bool
    first_message_id: Optional[int]
    stream_weekly_traffic: Optional[int]


class GetSubscriptionsResponse(BaseModel):
    subscriptions: List[SubscriptionResponse]


class TopicResponse(BaseModel):
    max_id: int
    name: str


class GetStreamTopicsResponse(BaseModel):
    msg: str
    result: str
    topics: List[TopicResponse]
