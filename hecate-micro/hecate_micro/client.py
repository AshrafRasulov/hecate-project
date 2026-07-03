import httpx
import random
import logging
from urllib.parse import urlparse
from hecate_micro.conf import hecate_settings

logger = logging.getLogger("hecate.client")

class HecateServiceClient:
    """Умный HTTP-клиент для вызова других микросервисов по их логическому имени"""
    
    def __init__(self):
        self._client = httpx.Client(timeout=10.0)

    def _resolve_url(self, url: str) -> str:
        parsed_url = urlparse(url)
        service_name = parsed_url.netloc  # Например: 'billing-api'
        
        try:
            # Спрашиваем у discovery-сервера актуальную карту сети
            response = self._client.get(f"{hecate_settings.DISCOVERY_URL}/api/v1/services")
            if response.status_code != 200:
                raise Exception("Cannot fetch registry from Hecate Discovery")
            
            registry = response.json()
            
            # Ищем инстансы для нужного нам микросервиса
            instances = registry.get(service_name, {})
            if not instances:
                raise Exception(f"Service '{service_name}' not found in Hecate registry")
            
            # Выбираем случайный живой инстанс (простейший Load Balancing - Round Robin / Random)
            chosen_instance = random.choice(list(instances.values()))["info"]
            
            # Собираем реальный физический URL
            real_netloc = f"{chosen_instance['host']}:{chosen_instance['port']}"
            resolved_url = parsed_url._replace(netloc=real_netloc).geturl()
            return resolved_url
            
        except Exception as e:
            logger.error(f"Hecate Service Resolution Error: {e}")
            # Если не смогли разрешить через реестр, пытаемся выполнить запрос как есть
            return url

    def get(self, url: str, *args, **kwargs):
        resolved_url = self._resolve_url(url)
        return self._client.get(resolved_url, *args, **kwargs)

    def post(self, url: str, *args, **kwargs):
        resolved_url = self._resolve_url(url)
        return self._client.post(resolved_url, *args, **kwargs)

# Expose a singleton instance for easy import and use across the Django project
hecate_http = HecateServiceClient()