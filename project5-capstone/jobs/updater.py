from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import job

def start():
    scheduler = BackgroundScheduler(daemon = True)
    scheduler.add_job(job,'interval',seconds = 10) #Fetch the news api for every user cofigs evey hour and 
    scheduler.start()                                #archive if there is an issue with config user config will
                                                     #be set to deactivated for resons that will be posted in info
                                                     #bar on front end and contet archiving stops 
                                                     #till the user reconfigs the settings
                                                     
    