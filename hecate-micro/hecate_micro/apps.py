from django.apps import AppConfig
import sys

class HecateMicroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hecate_micro'
    verbose_name = 'Hecate Microservice Client'

    def ready(self):
        # Check if the code is running during normal operation (not during management commands)
        # and not during automatic reloading (autoreloader) of Django
        if 'manage.py' in sys.argv and ('runserver' in sys.argv or 'gunicorn' in sys.argv):
            from hecate_micro.tasks.heartbeat import HeartbeatThread
            
            # Start the background daemon for monitoring host resources
            heartbeat_thread = HeartbeatThread()
            heartbeat_thread.start()