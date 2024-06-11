from django.db import models

# Create your models here.
class ScrapingJob(models.Model):
    job_id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ScrappingTask(models.Model):
    job = models.ForeignKey(ScrapingJob, related_name='tasks', on_delete=models.CASCADE)
    coin = models.CharField(max_length=10)
    output = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING')