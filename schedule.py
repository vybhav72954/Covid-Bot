from apscheduler.schedulers.blocking import BlockingScheduler
from covid_bot import *

scheduler = BlockingScheduler()

def the_funct():
    for numb in receiver_list:
        print(f"sending message to {numb}")
        send_message(numb, messages)

scheduler.add_job(the_funct, 'cron', minute='*/1')
scheduler.start()
