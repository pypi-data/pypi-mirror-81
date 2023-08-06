# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import Union, Optional, List, Dict, Any, Callable, Awaitable, TypeVar, Type
from uuid import uuid4
import asyncio

from mautrix.util.logging import TraceLogger

from .rpc import SignaldRPCClient
from .errors import UnexpectedError, UnexpectedResponse, make_linking_error
from .types import Address, Quote, Attachment, Reaction, Account, Message, Contact, Group, Profile

T = TypeVar('T')
EventHandler = Callable[[T], Awaitable[None]]


class SignaldClient(SignaldRPCClient):
    _event_handlers: Dict[Type[T], List[EventHandler]]

    def __init__(self, socket_path: str = "/var/run/signald/signald.sock",
                 log: Optional[TraceLogger] = None,
                 loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        super().__init__(socket_path, log, loop)
        self._event_handlers = {}
        self.add_rpc_handler("message", self._parse_message)

    def add_event_handler(self, event_class: Type[T], handler: EventHandler) -> None:
        self._event_handlers.setdefault(event_class, []).append(handler)

    def remove_event_handler(self, event_class: Type[T], handler: EventHandler) -> None:
        self._event_handlers.setdefault(event_class, []).remove(handler)

    async def _run_event_handler(self, event: T) -> None:
        try:
            handlers = self._event_handlers[type(event)]
        except KeyError:
            self.log.warning(f"No handlers for {type(event)}")
        else:
            for handler in handlers:
                try:
                    await handler(event)
                except Exception:
                    self.log.exception("Exception in event handler")

    async def _parse_message(self, data: Dict[str, Any]) -> None:
        event_type = data["type"]
        event_data = data["data"]
        event_class = {
            "message": Message,
        }[event_type]
        event = event_class.deserialize(event_data)
        await self._run_event_handler(event)

    async def subscribe(self, username: str) -> bool:
        try:
            await self.request("subscribe", "subscribed", username=username)
            return True
        except UnexpectedError as e:
            self.log.debug("Failed to subscribe to %s: %s", username, e)
            return False

    async def link(self, url_callback: Callable[[str], Awaitable[None]],
                   device_name: str = "mausignald") -> Account:
        req_id = uuid4()
        resp_type, resp = await self._raw_request("link", req_id, deviceName=device_name)
        if resp_type == "linking_error":
            raise make_linking_error(resp)
        elif resp_type != "linking_uri":
            raise UnexpectedResponse(resp_type, resp)

        self.loop.create_task(url_callback(resp["uri"]))

        resp_type, resp = await self._wait_response(req_id)
        if resp_type == "linking_error":
            raise make_linking_error(resp)
        elif resp_type != "linking_successful":
            raise UnexpectedResponse(resp_type, resp)

        return Account.deserialize(resp)

    async def list_accounts(self) -> List[Account]:
        data = await self.request("list_accounts", "account_list")
        return [Account.deserialize(acc) for acc in data["accounts"]]

    @staticmethod
    def _recipient_to_args(recipient: Union[Address, str]) -> Dict[str, Any]:
        if isinstance(recipient, Address):
            return {"recipientAddress": recipient.serialize()}
        else:
            return {"recipientGroupId": recipient}

    async def react(self, username: str, recipient: Union[Address, str],
                    reaction: Reaction) -> None:
        await self.request("react", "send_results", username=username,
                           reaction=reaction.serialize(),
                           **self._recipient_to_args(recipient))

    async def send(self, username: str, recipient: Union[Address, str], body: str,
                   quote: Optional[Quote] = None, attachments: Optional[List[Attachment]] = None,
                   timestamp: Optional[int] = None) -> None:
        serialized_quote = quote.serialize() if quote else None
        serialized_attachments = [attachment.serialize() for attachment in (attachments or [])]
        await self.request("send", "send_results", username=username, messageBody=body,
                           attachments=serialized_attachments, quote=serialized_quote,
                           timestamp=timestamp, **self._recipient_to_args(recipient))
        # TODO return something?

    async def mark_read(self, username: str, sender: Address, timestamps: List[int],
                        when: Optional[int] = None) -> None:
        await self.request_nowait("mark_read", username=username, timestamps=timestamps, when=when,
                                  recipientAddress=sender.serialize())

    async def list_contacts(self, username: str) -> List[Contact]:
        contacts = await self.request("list_contacts", "contact_list", username=username)
        return [Contact.deserialize(contact) for contact in contacts]

    async def list_groups(self, username: str) -> List[Group]:
        resp = await self.request("list_groups", "group_list", username=username)
        return [Group.deserialize(group) for group in resp["groups"]]

    async def get_profile(self, username: str, address: Address) -> Optional[Profile]:
        try:
            resp = await self.request("get_profile", "profile", username=username,
                                      recipientAddress=address.serialize())
        except UnexpectedResponse as e:
            if e.resp_type == "profile_not_available":
                return None
            raise
        return Profile.deserialize(resp)

    async def set_profile(self, username: str, new_name: str) -> None:
        await self.request("set_profile", "profile_set", username=username, name=new_name)
