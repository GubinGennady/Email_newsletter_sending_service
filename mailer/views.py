from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import CustomUser, Subscriber
from django.contrib.auth import logout, login
from .forms import SubscriberForm, MailingForm


class MailingsView(TemplateView):
    template_name = 'mailings.html'
class Index(TemplateView):
    template_name = 'index.html'


    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['object_list'] = HomeClient.objects.all()[:0]
    #     return context_data)
@method_decorator(csrf_exempt, name='dispatch')
class Register(TemplateView):

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        print(name, email, password)
        user = CustomUser.objects.create_user(email, email, password)
        login(request, user)
        return JsonResponse({
            'success': True
        })
@method_decorator(login_required, name='dispatch')
class Logout(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('/')

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context_data = {}
        context_data['form'] = SubscriberForm()
        context_data['subscribers'] = Subscriber.objects.filter(user=self.request.user)
        return context_data
    def post(self, request):
        form = SubscriberForm(request.POST)

        if form.is_valid():
            s = form.save(commit=False)
            s.user = request.user
            s.save()
            return redirect('/profile')
        return render(request, 'profile.html', {'form': form, 'subscribers': Subscriber.objects.filter(user=request.user)})

@login_required
def delete(request, id):
    if request.user.is_authenticated:
        Subscriber.objects.filter(id=id).delete()
    return redirect('/profile')

def create_mailing(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.save()  # Сохраняем рассылку
            form.save_m2m()  # Сохраняем связи ManyToMany (подписчиков)
            return redirect('mailings')  # Перенаправляем на страницу рассылок
    else:
        form = MailingForm()

    return render(request, 'create_mailing.html', {'form': form})