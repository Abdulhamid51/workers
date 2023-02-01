from .models import *
import datetime
from dateutil import rrule
import calendar

TODAY = datetime.datetime.now().strftime('%Y-%m-%d')

def get_sum_for_worker(request_user):
    worker = WorkerProfile.objects.get(user=request_user)
    days = Day.objects.filter(worker=worker)
    summa = 0
    for day in days:
        summa += day.sum
    worker.balance = summa
    worker.save()
    return True

def filter_history(date, worker):
    date = date.split('-')
    year = date[0]
    month = list(calendar.month_abbr).index(date[1])
    f_date = Day.objects.filter(date__year=year, date__month=month, worker=worker)
    return f_date


def year_month_iter(user_id):
    worker = WorkerProfile.objects.get(user=user_id)
    start = worker.date.date()
    # start = datetime.datetime(2022, 1, 1)
    end = datetime.datetime.now()
    date_list = []
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
        date_list.append(dt.strftime('%Y-%b'))
    return date_list


def create_daily_works(request_user):
    worker = WorkerProfile.objects.get(user=request_user)
    try:
        last_day = str(worker.days.last().date.date())
    except:
        last_day = '2000-12-12'

    if last_day == TODAY:
        day = Day.objects.filter(worker=worker).last()
    else:
        day = Day.objects.create(worker=worker)
        categories = WorkCategory.objects.all()
        for category in categories:
            Work.objects.create(day=day, category=category)
    return day
    

def work_counter(work_id, count):
    work = Work.objects.get(id=work_id)
    work.sum = work.category.price * count
    if work.category.type == 'dona':
        work.count = int(count)
    else:
        work.length = count
    work.save()
    return True

