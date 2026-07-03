from concurrent.futures import ThreadPoolExecutor, Future
import logging
from typing import Callable, Dict
from hecate_micro.resource.monitor import monitor

logger = logging.getLogger("hecate.balancer")

class HecateResourceBalancer:
    """Pull based Thread Pool Manager for internal Web-APIs. Dynamically adjusts thread allocations based on current resource usage."""
    
    def __init__(self):
        self._pools: Dict[str, ThreadPoolExecutor] = {}
        self._allocations: Dict[str, int] = {}

    def configure_pool(self, api_name: str, max_workers: int):
        """Creates or recreates a thread pool for a specific internal Web-API"""
        # Check current RAM usage and adjust max_workers if necessary
        metrics = monitor.get_current_metrics()
        if metrics["ram_used_mb"] > metrics["ram_total_mb"] * 0.85:
            logger.warning("Hecate Balancer: RAM usage is above 85%. Scaling down requested threads.")
            max_workers = max(2, max_workers // 2)  # OOM protection: reduce threads if RAM is high

        if api_name in self._pools:
            self._pools[api_name].shutdown(wait=False)
            
        logger.info(f"Hecate: Allocating {max_workers} OS-threads for '{api_name}' pool")
        self._pools[api_name] = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix=f"Hecate-{api_name}-"
        )
        self._allocations[api_name] = max_workers

    def execute(self, api_name: str, func: Callable, *args, **kwargs) -> Future:
        """Safely executes a heavy I/O task in the allocated thread pool"""
        if api_name not in self._pools:
            # If the pool for this API doesn't exist yet, create it with a default size
            self.configure_pool(api_name, max_workers=5)
            
        return self._pools[api_name].submit(func, *args, **kwargs)

    def get_allocations(self) -> Dict[str, int]:
        """Returns the current thread allocation map for sending to the server"""
        return self._allocations

hecate_balancer = HecateResourceBalancer()