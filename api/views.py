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
        serializer = DaysSerializer(day, many=False)
        return Response(serializer.data)
    
    def put(self, request):
        worker = WorkerProfile.objects.get(user=request.user)
        serializer = DaysSerializer(instance=worker, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"error":True})
        return Response(serializer.data)


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