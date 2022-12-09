from time import sleep
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from check_wallet_balance import run_scan

scheduler = BackgroundScheduler()

scheduler.add_job(
    run_scan,
    'interval',
    hours=3,
    next_run_time=datetime.datetime.now()
)

scheduler.start()

while True:
    sleep(1)