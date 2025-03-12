from django.urls import path

from mailer.views import Index, Register, Logout, ProfileView, delete, create_mailing

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('register/', Register.as_view(), name='register'),
    path('logout', Logout.as_view(), name='logout'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('delete/<int:id>', delete, name='delete'),
    path('mailings',create_mailing, name='mailings')
]