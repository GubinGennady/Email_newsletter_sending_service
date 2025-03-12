from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    dateBirthday = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)


class Subscriber(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя подписчика')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия подписчика')
    birth_date = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"


class Mailings(models.Model):
    subject = models.CharField(max_length=50, verbose_name='Тема рассылок')
    content = models.TextField(verbose_name='Текст рассылки')
    send_date = models.DateTimeField(verbose_name='Дата и время рассылки')
    is_sent = models.BooleanField(default=False)
    subscribers = models.ManyToManyField(Subscriber)

    def __str__(self):
        return self.subject


class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('Success', 'Успешно'),
        ('Failure', 'Ошибка'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(verbose_name='Ответ сервера')
    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, verbose_name='Рассылка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.mailing.subject} - {self.status}"
