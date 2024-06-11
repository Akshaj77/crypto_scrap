import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ScrapingJob, ScrappingTask  # Note the correction here (ScrappingTask -> ScrapingTask)
from .serializers import ScrapingJobSerializer, ScrapingTaskSerializer
from .tasks import scrape_coin_data

class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        if not all(isinstance(coin, str) for coin in coins):
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

        job = ScrapingJob.objects.create(job_id=uuid.uuid4())
        for coin in coins:
            task = ScrappingTask.objects.create(job=job, coin=coin)
            scrape_coin_data.delay(task.id)

        serializer = ScrapingJobSerializer(job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ScrapingStatusView(APIView):
    def get(self, request, pk=None):
        try:
            job = ScrapingJob.objects.get(job_id=pk)
        except ScrapingJob.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ScrapingJobSerializer(job)
        return Response(serializer.data)
