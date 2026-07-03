from django.conf import settings
import socket
import uuid

class HecateConfig:
    @property
    def DISCOVERY_URL(self) -> str:
        # Адрес сервера hecate-discovery
        return getattr(settings, "HECATE_DISCOVERY_URL", "http://127.0.0.1:8000")

    @property
    def APP_NAME(self) -> str:
        # Имя этого микросервиса в системе
        return getattr(settings, "HECATE_APP_NAME", "django-api-service")

    @property
    def INSTANCE_ID(self) -> str:
        # Уникальный ID конкретного инстанса (чтобы отличать реплики на хостинге)
        default_id = f"{socket.gethostname()}-{uuid.uuid4().hex[:8]}"
        return getattr(settings, "HECATE_INSTANCE_ID", default_id)

    @property
    def HOST(self) -> str:
        return getattr(settings, "HECATE_HOST", "127.0.0.1")

    @property
    def PORT(self) -> int:
        return getattr(settings, "HECATE_PORT", 8000)

    @property
    def HEARTBEAT_INTERVAL(self) -> int:
        # Как часто отправлять пульс на сервер (в секундах)
        return getattr(settings, "HECATE_HEARTBEAT_INTERVAL", 10)

hecate_settings = HecateConfig()