from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import *
from .funcs import *


class LoginView(LoginView):
    template_name = 'login.html'


class ListView(LoginRequiredMixin, View):
    def get(self, request):
        day = create_daily_works(request.user)
        works = Work.objects.filter(day=day)
        works_sum = 0
        for work in works:
            works_sum += work.sum
        day.sum = works_sum
        day.save()
        get_sum_for_worker(request.user)
        context = {
            'works':works,
            'day':day
            }
        return render(request, 'list.html', context)


class HistoryView(LoginRequiredMixin, View):
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
    def get(self, request):
        worker = WorkerProfile.objects.get(user=request.user)
        context = {
            "worker":worker
        }
        return render(request, 'profil.html', context)


def list_work_counter(request, id):
    value = request.GET.get('value')
    work = work_counter(id, float(value))
    return JsonResponse({'status':work})

