from speedcord import Client
from typing import Dict, Any, Optional, List, Union


class BaseContext:
    client: Client
    data: Dict[str, Any]

    def __init__(self, client: Client, data: Dict[str, Any]):
        ...


class MessageContext:
    id: int
    channel_id: int
    guild_id: Optional[int]
    author: Dict[str, Any]
    member: Optional[Dict[str, Any]]
    content: str
    timestamp: str
    edited_timestamp: Optional[str]
    tts: bool
    mention_everyone: bool
    mentions: Dict[str, Any]
    mention_roles: List[int]
    mention_channels: Dict[str, Any]
    attachments: List[Dict[str, Any]]
    embeds: List[Dict[str, Any]]
    reactions: List[Dict[str, Any]]
    nonce: Optional[Union[int, str]]
    pinned: bool
    webhook_id: Optional[int]
    type: int
    activity: Optional[Dict[str, Any]]
    application: Optional[Dict[str, Any]]
    message_reference: Optional[Dict[str, int]]
    flags: Optional[int]
    ...

    async def send(self, *, content: str = None, nonce: Union[int, str] = None, tts: bool = None,
                   embed: Dict[str, Any] = None, allowed_mentions: Dict[str, Any] = None):
        ...
