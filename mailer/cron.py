from django_cron import CronJobBase, Schedule
from .services import cronjob

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # Запускать каждую минуту

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'mailer.my_cron_job'  # Уникальный код задачи

    def do(self):
        cronjob()