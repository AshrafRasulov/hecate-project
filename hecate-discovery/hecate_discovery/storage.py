import time
from typing import Dict, Any
import threading

class MemoryRegistryStorage:
    def __init__(self):
        # Структура: { app_name: { instance_id: { data, last_seen } } }
        self._registry: Dict[str, Dict[str, dict]] = {}
        self._lock = threading.Lock()

    def register_or_update(self, app_name: str, instance_id: str, data: dict):
        """Регистрация нового инстанса или обновление его метрик при Heartbeat"""
        with self._lock:
            if app_name not in self._registry:
                self._registry[app_name] = {}
            
            self._registry[app_name][instance_id] = {
                "info": data,
                "last_seen": time.time()
            }

    def get_all_services(self) -> Dict[str, Dict[str, dict]]:
        """Возвращает карту всех активных сервисов"""
        with self._lock:
            return self._registry

    def clean_expired_services(self, ttl_seconds: int = 30):
        """Удаляет из реестра инстансы, которые не слали пульс дольше TTL"""
        now = time.time()
        with self._lock:
            apps_to_remove = []
            for app_name, instances in self._registry.items():
                instances_to_remove = [
                    inst_id for inst_id, inst_data in instances.items()
                    if now - inst_data["last_seen"] > ttl_seconds
                ]
                
                for inst_id in instances_to_remove:
                    del instances[inst_id]
                    print(f"[Hecate Discovery] Instance {inst_id} expired and removed from registry.")
                
                if not instances:
                    apps_to_remove.append(app_name)
            
            for app_name in apps_to_remove:
                del self._registry[app_name]

storage = MemoryRegistryStorage()