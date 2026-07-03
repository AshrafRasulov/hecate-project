from concurrent.futures import ThreadPoolExecutor, Future
import logging
from typing import Callable, Dict
from hecate_micro.resource.monitor import monitor

logger = logging.getLogger("hecate.balancer")

class HecateResourceBalancer:
    """Управляет пулами потоков, адаптируясь под ограничения RAM и CPU хостинга"""
    
    def __init__(self):
        self._pools: Dict[str, ThreadPoolExecutor] = {}
        self._allocations: Dict[str, int] = {}

    def configure_pool(self, api_name: str, max_workers: int):
        """Создает или пересоздает пул потоков для конкретного внутреннего Web-API"""
        # Проверяем текущую RAM перед расширением пула
        metrics = monitor.get_current_metrics()
        if metrics["ram_used_mb"] > metrics["ram_total_mb"] * 0.85:
            logger.warning("Hecate Balancer: RAM usage is above 85%. Scaling down requested threads.")
            max_workers = max(2, max_workers // 2)  # Защита от OOM: урезаем пул вдвое

        if api_name in self._pools:
            self._pools[api_name].shutdown(wait=False)
            
        logger.info(f"Hecate: Allocating {max_workers} OS-threads for '{api_name}' pool")
        self._pools[api_name] = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix=f"Hecate-{api_name}-"
        )
        self._allocations[api_name] = max_workers

    def execute(self, api_name: str, func: Callable, *args, **kwargs) -> Future:
        """Безопасно запускает тяжелую I/O задачу в выделенном пуле потоков"""
        if api_name not in self._pools:
            # Если пул не был настроен заранее, даем ему дефолтный лимит в 5 потоков
            self.configure_pool(api_name, max_workers=5)
            
        return self._pools[api_name].submit(func, *args, **kwargs)

    def get_allocations(self) -> Dict[str, int]:
        """Возвращает текущую карту распределения потоков для отправки на сервер"""
        return self._allocations

hecate_balancer = HecateResourceBalancer()