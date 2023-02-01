from rest_framework.views import APIView
from rest_framework.response import Response
from main.models import *
from main.funcs import *
from .serializers import *


class WorkListAPIView(APIView):

    def get(self, request):
        day = create_daily_works(request.user)
        serializer = DaysSerializer(day, many=False)
        return Response(serializer.data)


class HistoryAPIView(APIView):

    def get(self, request):
        worker = WorkerProfile.objects.get(user=request.user)
        try:
            filter = request.GET.get('filter')
            days = filter_history(filter, worker)
        except:
            days = Day.objects.filter(worker=worker)
            
        serializer = DaysSerializer(days, many=True)
        return Response(serializer.data)