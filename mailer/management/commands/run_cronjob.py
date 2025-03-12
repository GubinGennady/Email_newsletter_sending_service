from django.core.management.base import BaseCommand
from mailer.services import cronjob  # Импортируйте вашу функцию cronjob

class Command(BaseCommand):
    help = 'Запускает cronjob вручную'

    def handle(self, *args, **kwargs):
        cronjob()
        self.stdout.write(self.style.SUCCESS('Cronjob успешно запущен'))