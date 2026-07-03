from django.apps import AppConfig
import sys

class HecateMicroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hecate_micro'
    verbose_name = 'Hecate Microservice Client'

    def ready(self):
        # Проверяем, что код выполняется не во время служебных команд типа migrate или collectstatic
        # и не во время автоперезапуска (autoreloader) Django
        if 'manage.py' in sys.argv and ('runserver' in sys.argv or 'gunicorn' in sys.argv):
            from hecate_micro.tasks.heartbeat import HeartbeatThread
            
            # Запускаем фоновый демон-мониторинг ресурсов хоста
            heartbeat_thread = HeartbeatThread()
            heartbeat_thread.start()