from dataclasses import dataclass, field
from typing import Dict, Callable, Any


@dataclass
class Headers():

    size: int = int(2 ** 7)
    separator: str = "|"
    values_separator: str = "&"
    key_separator: str = "="

    data_header: str = "DATA"
    hello_header: str = "HELLO"
    accept_header: str = "ACCEPT"
    deny_header: str = "DENY"

    data_types_parsers: Dict[str, Callable] = field(default_factory=dict)


@dataclass
class Defaults():

    buffer_size: int = int(2 ** 13)
    timeout: float = 5
    peer_handlers: Dict[str, Callable] = field(default_factory=dict)
    connection_handlers: Dict[str, Callable] = field(default_factory=dict)


pinger_port: int = 1024
headers = Headers(data_types_parsers={
    "data_size": int,
    "buffer_size": int,
    "strict": bool
})
defaults = Defaults(peer_handlers={
    "listen": lambda peer: print(f"Peer listening for connections on {peer.address_name}!"),
    "offer": lambda connection: True,
    "stop": lambda peer: print(f"Peer ({peer.address_name}) stopped!")
})
