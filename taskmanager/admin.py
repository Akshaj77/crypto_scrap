from django.contrib import admin
from .models import ScrapingJob, ScrappingTask

admin.site.register(ScrapingJob)
admin.site.register(ScrappingTask)
