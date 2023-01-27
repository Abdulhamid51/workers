from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker')
    admin = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, related_name='workers')
    date = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField(default=0)
    got_balance = models.IntegerField(default=0)
    image = models.FileField(upload_to='profile_images/')

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

    def __str__(self):
        return str(self.date)


class Work(models.Model):
    category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, related_name='works')
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='theworks')
    count = models.IntegerField(default=0)
    length = models.FloatField(default=0)
    sum = models.IntegerField(default=0)

    def __str__(self):
        return str(self.category)


class BalanceHistory(models.Model):
    worker = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, related_name='balance_history')
    date = models.DateTimeField(auto_now_add=True)
    got_sum = models.IntegerField()

    def __str__(self):
        return str(self.date)


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         for user in User.objects.all():
#             if user.is_staff():
#                 admin = 
#                 worker = WorkerProfile.objects.create(user=instance, admin=admin)
        