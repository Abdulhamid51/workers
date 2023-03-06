from django.shortcuts import render, redirect, get_object_or_404
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
        categories = WorkCategory.objects.filter(admin=admin)
        balance = 0
        gave_balance = 0
        for history in BalanceHistory.objects.all():
            gave_balance += history.got_sum
        for worker in workers:
            balance += worker.balance
            create_daily_works(worker.user)
        admin.workers_money = balance
        admin.gave_money = gave_balance
        admin.save()
        context = {
            "admin":admin,
            "workers_b":workers.order_by('-balance')[:5],
            "categories":categories.order_by('-price')[:5],
        }
        return render(request, 'dashboard/index.html', context)
    

class PlanWorksView(LoginRequiredMixin, View):
    @is_staff
    def get(self, request):
        admin = AdminProfile.objects.get(user=request.user)
        context = {
            "admin":admin
        }
        return render(request, 'dashboard/planworks.html', context)


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
    
    @is_staff
    def post(self, request):
        try:
            work_name = request.POST.get('name')
            price = request.POST.get('price')
            type = request.POST.get('type')
            category = add_work(request.user, work_name, price, type)
            messages.success(request, 'Ish qo`shildi')
        except:
            messages.warning(request, 'Nimadur noto`g`ri ketdi')

        return render(request, 'dashboard/add_work.html')
    

class WorksListView(LoginRequiredMixin, View):
    @is_staff
    def get(self, request):
        try:
            c_id = int(request.GET.get("id"))
            category = WorkCategory.objects.get(id=c_id)
            category.delete()
            return redirect('/usta/works') 
        except:
            categories = WorkCategory.objects.filter(admin=request.user.admin)
            context = {
                'works':categories
            }
            return render(request, 'dashboard/works_list.html', context)
    
    @is_staff
    def post(self, request):
        c_id = int(request.POST.get("id"))
        name = request.POST.get("name")
        price = request.POST.get("price")
        category = WorkCategory.objects.get(id=c_id)
        category.name = name
        category.price = price
        category.save()
        return redirect('/usta/works')
    

class WorkersListView(LoginRequiredMixin, View):
    @is_staff
    def get(self, request):
        workers = WorkerProfile.objects.filter(admin=request.user.admin)
        context = {
            'workers':workers
        }
        return render(request, 'dashboard/workers_list.html', context)


class WorkerProfileView(LoginRequiredMixin, View):
    @is_staff
    def get(self, request, id):
        worker = get_object_or_404(WorkerProfile, id=id)
        context = {
            'worker':worker
        }
        return render(request, 'dashboard/detail.html', context)
    
    @is_staff
    def post(self, request, id):
        worker = get_object_or_404(WorkerProfile, id=id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        birth = request.POST.get('birth')
        address = request.POST.get('address')
        worker.user.first_name = first_name
        worker.user.last_name = last_name
        worker.user.username = phone
        worker.phone = phone
        worker.birth = birth
        worker.address = address
        worker.save()
        worker.user.save()
        return redirect(f'/usta/worker/{worker.id}')
        
    

class GiveMoneyHistoryListView(LoginRequiredMixin, View):
    @is_staff
    def get(self, request):
        try:
            w_id = request.GET.get('worker_id')
            worker = WorkerProfile.objects.get(id=w_id)
            balance = worker.balance
            return JsonResponse({"balance":balance})
        except:
            histories = BalanceHistory.objects.all().order_by('-id')
            context = {
                'histories':histories
            }
            return render(request, 'dashboard/history.html', context)
    
    @is_staff
    def post(self, request):
        admin = AdminProfile.objects.get(user=request.user)
        w = int(request.POST.get('worker'))
        worker = WorkerProfile.objects.get(id=w)
        price = int(request.POST.get('price'))
        BalanceHistory.objects.create(
            worker=worker,
            got_sum=price
        )
        worker.balance -= price
        worker.got_balance += price
        worker.save()
        admin.gave_money +=price
        admin.workers_money -= price
        admin.save()
        return redirect('/usta/give_money')



class BugWorksView(LoginRequiredMixin, View):
    @is_staff
    def get(self, request):
        bugs = BugWork.objects.all().order_by('-id')
        context = {
            'bugs':bugs
        }
        return render(request, 'dashboard/bug-works.html', context)
    
    @is_staff
    def post(self, request):
        admin = AdminProfile.objects.get(user=request.user)
        w = int(request.POST.get('worker'))
        worker = WorkerProfile.objects.get(id=w)
        price = int(request.POST.get('price'))
        info = str(request.POST.get('info'))
        BugWork.objects.create(
            worker=worker,
            price=price,
            info=info
        )
        worker.bugs_sum += price
        worker.save()
        admin.bugs_money +=price
        admin.save()
        return redirect('/usta/bugs')
    

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
    try:
        response = requests.request("POST", url)

        if response.json()['ok'] == True:
            admin.code = CODE
            admin.save()
            status = response.json()
        else:
            status = 'Xabar yuborilmadi'
    except:
        status = 'Bog`lanishda xato'

    return JsonResponse({"status":status})


def status_work(request):
    id = int(request.GET.get('id'))
    wid = int(request.GET.get('wid'))
    status = request.GET.get('status')
    worker = WorkerProfile.objects.get(id=wid)
    create_daily_works(worker.user)
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

def check_day(request):
    day = request.GET.get('day')
    if day == 'all':
        days = Day.objects.filter(date__date=TODAY)