from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
import requests

from .models import *
from .funcs import *
from .decorators import *


class ListView(LoginRequiredMixin, View):
    @is_worker
    def get(self, request):
        day = create_daily_works(request.user)
        works = Work.objects.filter(day=day)
        works_sum = 0
        for work in works:
            works_sum += work.sum
        day.worker.balance -= day.sum
        day.worker.balance += works_sum
        day.sum = works_sum
        day.save()
        day.worker.save()
        context = {
            'works':works,
            'day':day
            }
        return render(request, 'list.html', context)


class HistoryView(LoginRequiredMixin, View):
    @is_worker
    def get(self, request):
        worker = WorkerProfile.objects.get(user=request.user)
        try:
            filter = request.GET.get('filter')
            days = filter_history(filter, worker)
        except:
            days = Day.objects.filter(worker=worker)
        ls = year_month_iter(request.user.id)
        context = {
            'months':ls,
            'days':days.order_by('-id')
        }
        return render(request, 'history.html', context)


class ProfileView(LoginRequiredMixin, View):
    @is_worker
    def get(self, request):
        worker = WorkerProfile.objects.get(user=request.user)
        context = {
            "worker":worker
        }
        return render(request, 'profil.html', context)
    

class LoginView(View):
    @is_worker
    def get(self, request):
        return render(request, 'login.html')
    
    @is_worker
    def post(self, request):
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        worker = WorkerProfile.objects.get(phone=phone)
        username = worker.user.username
        password = worker.user.first_name+phone[:-5]
        if worker.code == int(code):
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                worker.code = 121232343423
                worker.save()
                return redirect('/')
            
        else:
            return redirect('/login')



def list_work_counter(request, id):
    value = request.GET.get('value')
    work = work_counter(id, float(value))
    return JsonResponse({'status':work})


def sms_send(request):
    
    USER_ID = '1257603816'
    MERCHANT_ID = 212
    TOKEN = 'THpraofsxAqQnkjOPEFSdmeLvRKNluhtbBZXVyIUGiDJYMg'
    CODE = code_generator()
    TEXT = f"Tasdiqlash kodi: {CODE}"
    
    try:
        phone = str(request.GET.get('phone'))
    except:
        phone = 'none'
    if phone.__len__() == 9:
        send_message_bot(TEXT+f"\nTelfon: {phone}")
        payload = json.dumps({
            "send": "",
            "text": TEXT,
            "number": phone,
            "user_id": USER_ID,
            "token": TOKEN,
            "id": MERCHANT_ID
        })
        worker = WorkerProfile.objects.get(phone=phone)
        url = "https://api.xssh.uz/smsv1/?data="+payload
        response = requests.request("POST", url)
        worker.code = CODE
        worker.save()
        status = 'Xabar yuborildi'
    else:
        status = 'Xabar yuborilmadi'

    return JsonResponse({"status":status})
