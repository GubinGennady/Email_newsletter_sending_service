# from datetime import datetime, timedelta
# from django.core.mail import send_mail
# from .models import Message, EmailLog
#
#
# def send_email(email):
#     """Эта функция отправляет все задания crontab-jobs, а также ведет журналы со статистикой."""
#     try:
#         send_mail(
#             subject=email.subject,
#             message=email.message,
#             recipient_list=[client.email for client in email.send_to_client.all()],
#             from_email=None
#         )
#         if email.frequency == 'Once':
#             email.status = 'Finished'
#         else:
#             email.status = 'Launched'
#         email.save()
#     except Exception as error:
#         email_log = EmailLog.objects.create(
#             status='Failure', server_response=error, email=email)
#         email_log.save()
#     else:
#         email_log = EmailLog.objects.create(
#             status='Success', server_response='Sent successfully', email=email)
#         email_log.save()
#
#
# def cronjob():
#     """Эта функция добавляет в crontab все электронные письма, чтобы мы могли отправлять их вовремя."""
#     # current_time = timezone.now()
#     cur_time = datetime.utcnow() + timedelta(hours=5)
#     emails = Message.objects.filter(
#         is_active=True,
#         status__in=['Created', 'Launched'],
#         start_time__lte=cur_time,  # Рассылка началась или должна начаться
#         end_time__gte=cur_time  # Рассылка не закончилась
#     ).exclude(status='Finished')
#
#     for email in emails:
#         if email.status == 'Created':
#             if email.frequency == 'Once':
#                 conditions_once(email, cur_time)
#             elif email.frequency == 'Daily':
#                 conditions_daily(email, cur_time)
#             elif email.frequency == 'Weekly':
#                 conditions_weekly(email, cur_time)
#             elif email.frequency == 'Monthly':
#                 conditions_monthly(email, cur_time)
#         elif email.status == 'Launched':
#             if email.frequency == 'Daily':
#                 conditions_daily(email, cur_time)
#             elif email.frequency == 'Weekly':
#                 conditions_weekly(email, cur_time)
#             elif email.frequency == 'Monthly':
#                 conditions_monthly(email, cur_time)
#
#
# def check_hour_minute(email, cur_time):
#     if email.send_datetime.hour == cur_time.hour:
#         if email.send_datetime.minute == cur_time.minute:
#             send_email(email)
#
#
# def conditions_once(email, cur_time):
#     if email.send_datetime.day == cur_time.day:
#         check_hour_minute(email, cur_time)
#
#
# def conditions_daily(email, cur_time):
#     check_hour_minute(email, cur_time)
#
#
# def conditions_weekly(email, cur_time):
#     if email.send_datetime.weekday() == cur_time.weekday():
#         check_hour_minute(email, cur_time)
#
#
# def conditions_monthly(email, cur_time):
#     if email.send_datetime.day == cur_time.day:
#         check_hour_minute(email, cur_time)


from django.core.mail import send_mail
from .models import Mailings, EmailLog
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Mailings


def send_email(mailing):
    """
    Отправляет рассылку на основе модели Mailings.
    Логирует результат отправки.
    """
    try:
        print('serv')
        # Отправка email
        send_mail(
            subject=mailing.subject,
            message=mailing.content,
            from_email=None,  # Используется EMAIL_HOST_USER из settings.py
            recipient_list=[subscriber.email for subscriber in mailing.subscribers.all()],
        )

        # Обновление статуса рассылки
        if mailing.is_sent:
            mailing.status = 'Finished'  # Если рассылка одноразовая
        else:
            mailing.status = 'Launched'  # Если рассылка периодическая
        mailing.save()

    except Exception as error:
        # Логирование ошибки
        EmailLog.objects.create(
            status='Failure',
            server_response=str(error),
            mailing=mailing
        )
    else:
        # Логирование успешной отправки
        EmailLog.objects.create(
            status='Success',
            server_response='Sent successfully',
            mailing=mailing
        )
def check_hour_minute(mailing, cur_time):
    """
    Проверяет, совпадает ли время отправки рассылки с текущим временем.
    """
    print(mailing.send_date.hour, cur_time.hour)
    print( mailing.send_date.minute,cur_time.minute)
    return (
            mailing.send_date.hour == cur_time.hour and
            mailing.send_date.minute == cur_time.minute
    )

def cronjob():
    """
    Проверяет рассылки, которые нужно отправить, и вызывает send_email.
    """
    # Текущее время с учетом часового пояса
    cur_time = timezone.now()

    # Получаем активные рассылки, которые нужно отправить
    mailings = Mailings.objects.filter(
        is_sent=False,  # Рассылка еще не отправлена
        send_date__lte=cur_time,  # Время отправки наступило
    )
    print(cur_time)

    for mailing in mailings:
        # Проверяем, нужно ли отправлять рассылку
        if check_hour_minute(mailing, cur_time):

            send_email(mailing)



