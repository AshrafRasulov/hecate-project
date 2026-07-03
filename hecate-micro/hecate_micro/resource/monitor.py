import os
import psutil
from typing import Dict

class HostResourceMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        
        # Вызываем один раз при инициализации, чтобы сбросить счетчик процентов CPU
        self.process.cpu_percent(interval=None)

    def get_current_metrics(self, pool_allocations: Dict[str, int] = None) -> dict:
        """Собирает оперативную информацию об утилизации ресурсов хостинга"""
        try:
            cpu_count = psutil.cpu_count(logical=True) or 1
            # Получаем % загрузки CPU текущим процессом с момента последнего вызова
            cpu_usage = self.process.cpu_percent(interval=None)
            
            # RAM хостинга и RAM процесса (в Мегабайтах)
            virtual_mem = psutil.virtual_memory()
            ram_total_mb = virtual_mem.total // (1024 * 1024)
            ram_used_mb = self.process.memory_info().rss // (1024 * 1024)
            
            # Количество активных ОС-потоков внутри процесса Django
            active_threads = self.process.num_threads()
            
        except Exception:
            # Фолбэк на случай ограничений прав доступа в некоторых контейнерах
            cpu_count = 1
            cpu_usage = 0.0
            ram_total_mb = 0
            ram_used_mb = 0
            active_threads = 1

        return {
            "cpu_count": cpu_count,
            "cpu_usage_percent": round(cpu_usage, 2),
            "ram_total_mb": ram_total_mb,
            "ram_used_mb": ram_used_mb,
            "active_threads": active_threads,
            "pool_allocations": pool_allocations or {}
        }

monitor = HostResourceMonitor()