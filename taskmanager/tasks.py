from celery import shared_task
from .models import ScrappingTask
from .scrapper import CoinMarketCapScraper

@shared_task
def scrape_coin_data(task_id):
    task = ScrappingTask.objects.get(id=task_id)
    scraper = CoinMarketCapScraper(task.coin)
    try:
        data = scraper.fetch_data()
        task.output = data
        print("data")
        task.status = 'COMPLETED'
    except Exception as e:
        task.status = 'FAILED'
    task.save()
