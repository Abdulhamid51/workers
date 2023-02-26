from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import is_staff
from django.contrib.auth.views import LoginView
from main.models import *
from main.funcs import *
from django.contrib import messages
import requests
import json


class LoginView(LoginView):
    template_name = 'dashboard/login.html'


class HomePageView(LoginRequiredMixin, View):
    @is_staff
    def get(self, request):
        admin = AdminProfile.objects.get(user=request.user)
        workers = WorkerProfile.objects.filter(admin=admin)
        for worker in workers:
            create_daily_works(worker.user)
        context = {
            "admin":admin
        }
        return render(request, 'dashboard/index.html', context)


class AddWorkerView(LoginRequiredMixin, View):
    @is_staff
    def get(self, request):
        return render(request, 'dashboard/add_worker.html')
    
    @is_staff
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        birth = request.POST.get('birth')
        address = request.POST.get('address')
        admin = AdminProfile.objects.get(user=request.user)
        if int(code) == admin.code:
            status = create_workerprofile(
                admin_user=admin,
                phone=phone,
                f_name=first_name,
                l_name=last_name,
                birth=birth,
                address=address
            )
            messages.info(request, status)
            admin.code = 1012394949
            admin.save()
        else:
            messages.error(request, 'Tasdiqlash kodi noto`g`ri')

        return render(request, 'dashboard/add_worker.html')
    

class AddWorkView(LoginRequiredMixin, View):
    @is_staff
    def get(self, request):
        return render(request, 'dashboard/add_work.html')
    

def sms_send(request):
    phone = request.GET.get('phone')
    admin_id = request.GET.get('id')
    admin = AdminProfile.objects.get(id=admin_id)
    USER_ID = '1257603816'
    MERCHANT_ID = 212
    TOKEN = 'THpraofsxAqQnkjOPEFSdmeLvRKNluhtbBZXVyIUGiDJYMg'
    CODE = code_generator()
    TEXT = f"Tasdiqlash kodi: {CODE}"
    

    payload = json.dumps({
        "send": "",
        "text": TEXT,
        "number": phone,
        "user_id": USER_ID,
        "token": TOKEN,
        "id": MERCHANT_ID
    })

    url = "https://api.xssh.uz/smsv1/?data="+payload

    response = requests.request("POST", url)

    print(response.json())

    if response.json()['ok'] == True:
        admin.code = CODE
        admin.save()
        status = 'Xabar yuborildi'
    else:
        status = 'Nimadur xato ketdi'

    return JsonResponse({"status":status})


def status_work(request):
    id = int(request.GET.get('id'))
    wid = int(request.GET.get('wid'))
    status = request.GET.get('status')
    worker = WorkerProfile.objects.get(id=wid)
    category = WorkCategory.objects.get(id=id)
    work = Work.objects.filter(day__worker=worker, category=category).last()
    if status == 'true':
        work.active = True
        worker.works.add(category)
        response = 'added work'

    elif status == 'false':
        work.active = False
        worker.works.remove(category)
        response = 'removed work'
    
    work.save()
    worker.save()
    return JsonResponse({"response":response})