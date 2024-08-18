from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .services import *


@shared_task
def update_posts(from_page, to_page):
    urls = extract_page_links(from_page, to_page)
    create_posts(urls)
    return urls
