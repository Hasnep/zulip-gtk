from pydantic import BaseModel, Field
from typing import List, Optional, Union


class ReactionResponse(BaseModel):
    emoji_code: str
    emoji_name: str
    reaction_type: str
    unicode_emoji: str
    realm_emoji: str
    zulip_extra_emoji: str
    user_id: str


class TopicLinksResponse(BaseModel):
    text: str
    url: str


class MessageResponse(BaseModel):
    avatar_url: Optional[str]
    client: str
    content: str
    content_type: str
    display_recipient: Union[str, dict]
    _id: int = Field(..., alias="id")
    is_me_message: bool
    # reactions: List[ReactionResponse]
    recipient_id: int
    sender_email: str
    sender_full_name: str
    sender_id: int
    sender_realm_str: str
    stream_id: int
    subject: str
    topic_links: List[TopicLinksResponse]
    submessages: List[str]
    timestamp: int
    _type: str = Field(..., alias="type")
    flags: List[str]
    last_edit_timestamp: Optional[int]
    match_content: Optional[str]
    match_subject: Optional[str]


class GetMessagesResponse(BaseModel):
    anchor: Optional[int]
    found_anchor: Optional[bool]
    found_newest: Optional[bool]
    found_oldest: Optional[bool]
    history_limited: Optional[bool]
    messages: Optional[List[MessageResponse]]
