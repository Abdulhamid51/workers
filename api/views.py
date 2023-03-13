from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import *
from main.funcs import *
from .serializers import *


class WorkListAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
        work_serializer = WorksSerializer(works, many=True)
        day_serializer = DaysSerializer(day, many=False)
        return Response({"day":day_serializer.data,"works":work_serializer.data})
    
    def put(self, request):
        works = request.data['works']
        for work in works:
            work_obj = Work.objects.get(id=work['id'])
            work_obj.count = work['count']
            work_obj.length = work['length']
            work_obj.sum = work['sum']
            work_obj.save()
        return Response({"ok":True})


class HistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        worker = WorkerProfile.objects.get(user=request.user)
        try:
            filter = request.GET.get('filter')
            days = filter_history(filter, worker)
        except:
            days = Day.objects.filter(worker=worker)
            
        serializer = DaysSerializer(days, many=True)
        return Response(serializer.data)