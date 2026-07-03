# hecate_micro/resource/balancer.py
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)

class HecateResourceBalancer:
    def __init__(self):
        # Хранилище пулов для разных внутренних модулей API
        self._pools = {}

    def configure_pool(self, api_name: str, max_workers: int):
        """Динамически настраивает или изменяет размер пула для конкретного Web-API"""
        logger.info(f"Hecate: Allocating {max_workers} threads for {api_name}")
        self._pools[api_name] = ThreadPoolExecutor(
            max_workers=max_workers, 
            thread_name_prefix=f"Hecate-{api_name}-"
        )

    def execute_in_pool(self, api_name: str, func, *args, **kwargs):
        """Запускает задачу в строго выделенном пуле потоков для этого API"""
        if api_name not in self._pools:
            # Дефолтный минимальный пул, если не настроен явно
            self.configure_pool(api_name, max_workers=5)
        
        return self._pools[api_name].submit(func, *args, **kwargs)