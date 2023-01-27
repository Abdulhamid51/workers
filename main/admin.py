from django.contrib import admin
from .models import *

admin.site.register(AdminProfile)
admin.site.register(WorkerProfile)
admin.site.register(WorkCategory)
admin.site.register(Day)
admin.site.register(Work)
admin.site.register(BalanceHistory)