import secrets

from django.db import models

from django.contrib.auth.models import AbstractUser

NULLABLE = {'null': True, 'blank': True}


class CustomUser(AbstractUser):
    dateBirthday = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, **NULLABLE)


class Subscriber(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя подписчика')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия подписчика')
    birth_date = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    unsubscribe_token = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, **NULLABLE, verbose_name='Связанный пользователь')

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}"

    def save(self, *args, **kwargs):
        if not self.unsubscribe_token:
            self.unsubscribe_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ['-subscribed_at']


# class Subscriber(models.Model):
#     first_name = models.CharField(max_length=100, verbose_name='Имя подписчика')
#     last_name = models.CharField(max_length=100, verbose_name='Фамилия подписчика')
#     birth_date = models.DateField(verbose_name='Дата рождения')
#     email = models.EmailField(unique=True, verbose_name='Электронная почта')
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, **NULLABLE)
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name} {self.email}"


class Mailings(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    subject = models.CharField(max_length=255, verbose_name='Тема рассылок')
    content = models.TextField(verbose_name='Текст рассылки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    send_date = models.DateTimeField(verbose_name='Дата и время рассылки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    subscribers = models.ManyToManyField(Subscriber, verbose_name='Получатели', limit_choices_to={'is_active': True})
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Создано')

    def __str__(self):
        return f"{self.subject} ({self.status})"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-send_date']


# class Mailings(models.Model):
#     subject = models.CharField(max_length=50, verbose_name='Тема рассылок')
#     content = models.TextField(verbose_name='Текст рассылки')
#     send_date = models.DateTimeField(verbose_name='Дата и время рассылки')
#     is_sent = models.BooleanField(default=False)
#     subscribers = models.ManyToManyField(Subscriber)
#
#     def __str__(self):
#         return self.subject
#
#     class Meta:
#         verbose_name = 'Рассылка'
#         verbose_name_plural = 'Рассылки'


class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
    ]

    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, related_name='logs',
                                verbose_name='Кем рассылка')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name='Получатель')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(verbose_name='Ответ сервера')
    opened_at = models.DateTimeField(**NULLABLE, verbose_name='Дата открытие')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.mailing.subject} {self.subscriber.email} ({self.status})"

    class Meta:
        verbose_name = 'Журнал электронной почты'
        verbose_name_plural = 'Журналы электронных почт'
        ordering = ['-created_at']

# class EmailLog(models.Model):
#     STATUS_CHOICES = [
#         ('Success', 'Успешно'),
#         ('Failure', 'Ошибка'),
#     ]
#
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
#     server_response = models.TextField(verbose_name='Ответ сервера')
#     mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, verbose_name='Рассылка')
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
#
#     def __str__(self):
#         return f"{self.mailing.subject} - {self.status}"
