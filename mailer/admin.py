from django.contrib import admin
from .models import CustomUser, Mailings, Subscriber, EmailLog

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Mailings)
admin.site.register(Subscriber)
admin.site.register(EmailLog)