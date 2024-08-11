from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
import requests
import django
import environ
import os

env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(__file__), '..', '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technews.settings')
django.setup()

from news.models import News
from tags.models import Tag


def extract_links(from_page: int, to_page: int) -> list[WebElement]:
    """
     Extracts a list of article links from the specified pages of the website.

     Args:
         from_page (int): The starting page number.
         to_page (int): The ending page number.

     Returns:
         list[WebElement]: A list of web elements representing the article links.
     """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(env('CHROMEDRIVER_PATH'))
    wd = webdriver.Chrome(service=service)
    links = []
    try:
        for i in range(to_page - from_page + 1):
            url = f"https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber={from_page+i}"
            wd.get(url)
            wd.implicitly_wait(5)
            post_links = wd.find_elements(By.XPATH,
                                          "//a[contains(@class, 'BrowseArticleListItemDesktop__WrapperLink')]")
            for i in range(len(post_links)):
                post_links[i] = post_links[i].get_attribute('href')
            links.extend(post_links)
    finally:
        wd.quit()

    return links


def create_single_post(url: str) -> None:
    """
    Creates a single news post in the database by extracting the necessary information from the given URL.

    Args:
        url (str): The URL of the news article to extract and save.
    """
    response = requests.get(url)
    tags = []
    content = BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 200:
        labels = content.find_all(attrs={'class': 'typography__StyledDynamicTypographyComponent-t787b7-0 cHbulB'})

        # extract the post's tags
        for label in labels:
            tag, created = Tag.objects.get_or_create(label=label.text)
            tags.append(tag)

        # extract the post's title
        title = content.find('h1')

        # extract the post's author
        source = content.find(class_="typography__StyledDynamicTypographyComponent-t787b7-0 kZjgvK").text

        # extract the post's body
        paragraphs = content.find_all(attrs={'class': 'ParagraphElement__ParagraphBase-sc-1soo3i3-0'})
        text = "\n".join(f"{p.text}" for p in paragraphs)
        print(text)

        news = News.objects.create(
            title=title,
            content=text,
            source=source,
        )

        [news.tags.add(tag) for tag in tags]


def create_multiple_posts(urls: list[str]) -> None:
    """
    Creates multiple news posts in the database by extracting information from a list of URLs.

    Args:
        urls (list[str]): A list of URLs to process and create news posts from.
    """
    for url in urls:
        create_single_post(url)
