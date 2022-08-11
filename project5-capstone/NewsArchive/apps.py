from turtle import update
from django.apps import AppConfig
import os

class NewsarchiveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NewsArchive'

    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE') 
        if run_once is not None:
            return 
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True' 
        from jobs import updater
        updater.start()
       
        
      
