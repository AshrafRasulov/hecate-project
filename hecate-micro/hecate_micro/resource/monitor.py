import os
import psutil
from typing import Dict

class HostResourceMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        
        # call cpu_percent once to initialize the internal state of psutil
        self.process.cpu_percent(interval=None)

    @staticmethod  # This method can be static because it doesn't depend on instance variables
    def get_current_metrics() -> Dict[str, int]:
        process = psutil.Process(os.getpid())
        
        # 1. Check CPU: custom allocation or automatic
        if hecate_settings.CUSTOM_CPU_COUNT is not None:
            cpu_count = hecate_settings.CUSTOM_CPU_COUNT
        else:
            cpu_count = psutil.cpu_count(logical=True)

        # 2. Check RAM: Manual override or automatic detection
        if hecate_settings.CUSTOM_RAM_TOTAL is not None:
            ram_total = hecate_settings.CUSTOM_RAM_TOTAL
        else:
            ram_total = psutil.virtual_memory().total // (1024 * 1024)

        # Currently used memory by the process (keeping it real-time to observe overloads)
        ram_used = process.memory_info().rss // (1024 * 1024)
        cpu_usage = process.cpu_percent(interval=None)

        # Additionally, we can include pool allocation info if needed
        pool_alloc = {}
        if hecate_settings.CPU_CORE_ASSIGNMENT:
            pool_alloc["cpu_assignment_mask"] = hecate_settings.CPU_CORE_ASSIGNMENT

        return {
            "cpu_count": cpu_count,
            "cpu_usage_percent": cpu_usage,
            "ram_total_mb": ram_total,
            "ram_used_by_app_mb": ram_used,
            "active_threads": process.num_threads(),
            "pool_allocations": pool_alloc
        }

monitor = HostResourceMonitor()