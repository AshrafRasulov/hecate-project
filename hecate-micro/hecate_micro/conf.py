import os
import socket
import uuid
from configparser import ConfigParser
from django.conf import settings

class HecateConfig:
    def __init__(self):
        self.ini_config = ConfigParser()
        # Looking for the hecate.ini file in the user's project root directory
        self.ini_path = os.path.join(os.getcwd(), "hecate.ini")
        if os.path.exists(self.ini_path):
            self.ini_config.read(self.ini_path)

    def _get_ini_value(self, section: str, key: str, default=None):
        if self.ini_config.has_option(section, key):
            return self.ini_config.get(section, key)
        return default

    @property
    def DISCOVERY_URL(self) -> str:
        return getattr(settings, "HECATE_DISCOVERY_URL", self._get_ini_value("HECATE", "discovery_url", "http://127.0.0.1:8771"))

    @property
    def APP_NAME(self) -> str:
        return getattr(settings, "HECATE_APP_NAME", self._get_ini_value("HECATE", "app_name", "django-api-service"))

    @property
    def INSTANCE_ID(self) -> str:
        default_id = f"{socket.gethostname()}-{uuid.uuid4().hex[:8]}"
        return getattr(settings, "HECATE_INSTANCE_ID", self._get_ini_value("HECATE", "instance_id", default_id))

    @property
    def HOST(self) -> str:
        return getattr(settings, "HECATE_HOST", self._get_ini_value("HECATE", "host", "127.0.0.1"))

    @property
    def PORT(self) -> int:
        return int(getattr(settings, "HECATE_PORT", self._get_ini_value("HECATE", "port", 8772)))

    @property
    def HEARTBEAT_INTERVAL(self) -> int:
        return int(getattr(settings, "HECATE_HEARTBEAT_INTERVAL", self._get_ini_value("HECATE", "heartbeat_interval", 10)))

    # --- NEW PARAMETERS FOR RESOURCE LIMITATION ---
    @property
    def CUSTOM_CPU_COUNT(self) -> int | None:
        val = self._get_ini_value("RESOURCES", "cpu_count")
        return int(val) if val else None

    @property
    def CUSTOM_RAM_TOTAL(self) -> int | None:
        val = self._get_ini_value("RESOURCES", "ram_total_mb")
        return int(val) if val else None

    @property
    def CPU_CORE_ASSIGNMENT(self) -> str | None:
        """Returns a string like '0,1' to assign specific CPU cores to the Django process."""
        return self._get_ini_value("RESOURCES", "cpu_assignment")

hecate_settings = HecateConfig()