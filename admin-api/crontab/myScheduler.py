import datetime
import os
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from config import config

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

run_date = datetime.datetime.now() + datetime.timedelta(seconds=20)


@register_job(scheduler, "cron", id=uuid.uuid4().hex, hour=1, minute=30, replace_existing=True,
              timezone='Asia/Shanghai')
def setUp_database_scheduler():
    pass


register_events(scheduler)
scheduler.start()
