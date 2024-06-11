from rest_framework import serializers
from .models import ScrapingJob, ScrappingTask

class ScrapingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrappingTask
        fields = '__all__'

class ScrapingJobSerializer(serializers.ModelSerializer):
    tasks = ScrapingTaskSerializer(many=True, read_only=True)

    class Meta:
        model = ScrapingJob
        fields = '__all__'
