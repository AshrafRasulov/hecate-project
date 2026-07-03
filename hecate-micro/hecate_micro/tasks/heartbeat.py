import threading
import time
import logging
import httpx
from hecate_micro.conf import hecate_settings
from hecate_micro.resource.monitor import monitor

logger = logging.getLogger("hecate.heartbeat")

class HeartbeatThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True  # Поток автоматически завершится при остановке Django
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        logger.info("Hecate: Background heartbeat thread started.")
        
        # Даем Django полностью инициализироваться перед началом отправки
        time.sleep(2)
        
        # Сначала регистрируем микросервис
        self._register_service()

        while not self._stop_event.is_set():
            try:
                # Собираем актуальные метрики RAM/CPU/Потоков
                current_metrics = monitor.get_current_metrics()
                
                payload = {
                    "instance_id": hecate_settings.INSTANCE_ID,
                    "app_name": hecate_settings.APP_NAME,
                    "metrics": current_metrics
                }
                
                # Шлем POST-запрос пульса на hecate-discovery
                with httpx.Client(timeout=3.0) as client:
                    response = client.post(
                        f"{hecate_settings.DISCOVERY_URL}/api/v1/heartbeat", 
                        json=payload
                    )
                    if response.status_code != 200:
                        logger.warning(f"Hecate Discovery responded with code {response.status_code}")
            except Exception as e:
                logger.error(f"Hecate: Failed to send heartbeat to discovery server: {e}")
            
            # Спим заданный интервал секунд
            time.sleep(hecate_settings.HEARTBEAT_INTERVAL)

    def _register_service(self):
        """Метод первичной регистрации инстанса при старте"""
        try:
            payload = {
                "app_name": hecate_settings.APP_NAME,
                "instance_id": hecate_settings.INSTANCE_ID,
                "host": hecate_settings.HOST,
                "port": hecate_settings.PORT,
                "status": "UP",
                "metrics": monitor.get_current_metrics()
            }
            with httpx.Client(timeout=5.0) as client:
                response = client.post(
                    f"{hecate_settings.DISCOVERY_URL}/api/v1/register", 
                    json=payload
                )
                if response.status_code == 200 or response.status_code == 201:
                    logger.info(f"Hecate: Successfully registered service {hecate_settings.APP_NAME}")
                else:
                    logger.error(f"Hecate Registration failed. Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Hecate: Service registration error: {e}")