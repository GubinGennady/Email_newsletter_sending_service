from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
import logging

from mailing import settings
from .models import Mailings

logger = logging.getLogger(__name__)

@shared_task
def check_mailing_and_send_reminders():
    logger.info('Задача check_mailing_and_send_reminders запущена')

    habits = Mailings.objects.select_related('user').all()
    if not habits:
        logger.info('Нет активных рассылок')
        return

    for mailing in habits:
        if mailing.is_active:
            logger.info(f'Отправка письма на {mailing.email}')
            send_email_reminder(mailing.email, mailing)

@shared_task
def send_email_reminder(email, mailing):
    """Функция отправки email-напоминания"""
    try:
        send_mail(
            subject='Время завершить свою привычку!',
            message=f'Пришло время выполнить свою привычку: {mailing.is_active}. '
                    f'Вы указывали, что это должно быть сделано каждый день.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f'Письмо успешно отправлено на {email}')
    except Exception as e:
        logger.error(f'Ошибка при отправке письма на {email}: {e}')
