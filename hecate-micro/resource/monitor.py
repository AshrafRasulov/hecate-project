# hecate_micro/resource/monitor.py
import psutil
import os

class HostResourceMonitor:
    @staticmethod
    def get_current_metrics():
        process = psutil.Process(os.getpid())
        return {
            "cpu_count": psutil.cpu_count(logical=True),
            "cpu_usage_percent": process.cpu_percent(interval=None),
            "ram_total_mb": psutil.virtual_memory().total // (1024 * 1024),
            "ram_used_by_app_mb": process.memory_info().rss // (1024 * 1024),
            "active_threads": process.num_threads()
        }