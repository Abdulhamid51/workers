from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    date = models.DateTimeField(auto_now_add=True)
    gave_money = models.IntegerField(default=0)
    workers_money = models.IntegerField(default=0)
    bugs_money = models.IntegerField(default=0)

    code = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker')
    admin = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, related_name='workers')
    date = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField(default=0)
    got_balance = models.IntegerField(default=0)
    bugs_sum = models.IntegerField(default=0)
    image = models.FileField(upload_to='profile_images/', blank=True, null=True)

    birth = models.DateField(blank=True)
    phone = models.PositiveIntegerField()
    address = models.CharField(blank=True, max_length=250)
    active = models.BooleanField(default=True)

    code = models.IntegerField(default=0)

    works = models.ManyToManyField('main.WorkCategory', blank=True, related_name='category_workers')

    def __str__(self):
        return self.user.username


class WorkCategory(models.Model):
    WORK_TYPES = (
        ("dona","dona"),
        ("metr","metr"),
    )

    name = models.CharField(max_length=200)
    admin = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, related_name='work_categories')
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    type = models.CharField(choices=WORK_TYPES, max_length=4)

    def __str__(self):
        return self.name


class Day(models.Model):
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name='days')
    date = models.DateTimeField(auto_now_add=True)
    sum = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.date)


class Work(models.Model):
    category = models.ForeignKey(WorkCategory, on_delete=models.SET_NULL, related_name='works', null=True)
    active = models.BooleanField(default=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='theworks')
    count = models.IntegerField(default=0)
    length = models.FloatField(default=0)
    sum = models.IntegerField(default=0)

    def __str__(self):
        return str(self.category)


class BalanceHistory(models.Model):
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name='balance_history')
    date = models.DateTimeField(auto_now_add=True)
    got_sum = models.IntegerField()

    def __str__(self):
        return str(self.date)
    

class BugWork(models.Model):
    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE, related_name='bugs')
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0)
    info = models.CharField(max_length=350)

    def __str__(self):
        return self.info


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         for user in User.objects.all():
#             if user.is_staff():
#                 admin = 
#                 worker = WorkerProfile.objects.create(user=instance, admin=admin)
        