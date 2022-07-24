from typing import ClassVar

__all__: list[str] = ["GatewayEvents"]

class GatewayEvents:
    HEARTBEAT: ClassVar[int] = 0
    HEARBEAT_ACK: ClassVar[int] = 1
    USER_CREATE: ClassVar[int] = 2
    USER_UPDATE: ClassVar[int] = 3
    USER_DELETE: ClassVar[int] = 4
    MESSAGE_CREATE: ClassVar[int] = 5
    MESSAGE_UPDATE: ClassVar[int] = 6
    MESSAGE_DELETE: ClassVar[int] = 7
    ADMIN_SETTINGS_UPDATE: ClassVar[int] = 8
    IDENTIFY: ClassVar[int] = 9

    @classmethod
    def all_events(cls) -> list[str]:
        return [attr for attr in dir(cls) if not attr.startswith("_")]