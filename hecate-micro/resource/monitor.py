import os
import psutil
from typing import Dict, Any
from hecate_micro.conf import hecate_settings

class HostResourceMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        # Initialize CPU percent to avoid getting 0.0 on the first call
        self.process.cpu_percent(interval=None)

    @staticmethod
    def get_current_metrics() -> Dict[str, Any]:
        process = psutil.Process(os.getpid())
        
        # 1. Check CPU: custom allocation or automatic
        if hecate_settings.CUSTOM_CPU_COUNT is not None:
            cpu_count = hecate_settings.CUSTOM_CPU_COUNT
        else:
            cpu_count = psutil.cpu_count(logical=True) or 1

        # 2. Check RAM: custom allocation or automatic
        if hecate_settings.CUSTOM_RAM_TOTAL is not None:
            ram_total = hecate_settings.CUSTOM_RAM_TOTAL
        else:
            ram_total = psutil.virtual_memory().total // (1024 * 1024)

        # Get actual process metrics in megabytes
        ram_used = process.memory_info().rss // (1024 * 1024)
        cpu_usage = process.cpu_percent(interval=None)

        # Extract CPU core allocation mask (e.g., 1:1:6)
        pool_alloc = {}
        if hecate_settings.CPU_CORE_ASSIGNMENT:
            pool_alloc["cpu_assignment_mask"] = hecate_settings.CPU_CORE_ASSIGNMENT

        return {
            "cpu_count": cpu_count,
            "cpu_usage_percent": round(cpu_usage, 2),
            "ram_total_mb": ram_total,
            "ram_used_by_app_mb": ram_used,
            "active_threads": process.num_threads(),
            "pool_allocations": pool_alloc
        }

monitor = HostResourceMonitor()