import sys

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from services.utility import check_number_in_geofence
import secrets

token = secrets.token_urlsafe(20)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'AddAttendance') 
    scheduler.add_job(func=check_number_in_geofence, id=f"Attendance {token}", trigger='interval', minutes=2, hour=0, name='attendance', jobstore='AddAttendance')
    register_events(scheduler)
    scheduler.start()
    print('Geofence Started!!!!', file=sys.stdout)
