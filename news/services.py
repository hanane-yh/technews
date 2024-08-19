from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from news.models import News
from tags.models import Tag
import requests
import environ


env = environ.Env()
def extract_page_links(from_page: int, to_page: int) -> list[str]:
    """
     Extracts a list of article links from the specified pages of the website.

     Args:
         from_page (int): The starting page number.
         to_page (int): The ending page number.

     Returns:
         list[str]: A list of the article links.
     """
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    chrome_wd = webdriver.Remote(command_executor=env('HUB_URL'), options=chrome_options)
    links = []
    try:
        for i in range(to_page - from_page + 1):
            url = f"https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber={from_page + i}"
            chrome_wd.get(url)
            chrome_wd.implicitly_wait(5)
            link_elements = chrome_wd.find_elements(By.XPATH,
                                             "//a[contains(@class, 'BrowseArticleListItemDesktop__WrapperLink')]")
            extracted_links = [link.get_attribute('href') for link in link_elements]
            links.extend(extracted_links)
    except Exception as e:
        print(f"Error happened while extracting links. error message: {e}")
    finally:
        chrome_wd.quit()

    return links


def extract_content(url: str) -> tuple[str, str, str, list[str]] | None:
    """
    Extracts content from a given URL, including the title, text, source, and labels of a post.

    Args:
        url (str): The URL of the web page from which to extract content.

    Returns:
        tuple[str, str, str, list[str]] | None:
            A tuple containing:
            - title (str): The title of the post. Defaults to "default title" if not found.
            - text (str): The main content of the post, concatenated from multiple paragraphs.
            - source (str): The source or author of the post. Returns an empty string if not found.
            - labels (list[str]): A list of strings representing the tags associated with the post.

            Returns `None` if the HTTP response status code is not 200 (indicating a failed request).
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code != 200:
        print(f"request failed for {url}")
        return

    # extract the post's tags
    labels = soup.find_all(attrs={'class': 'typography__StyledDynamicTypographyComponent-t787b7-0 cHbulB'})

    # extract the post's title
    title = soup.find('h1').text if soup.find('h1') is not None else "default title"

    # extract the post's author
    content = soup.find(class_="typography__StyledDynamicTypographyComponent-t787b7-0 kZjgvK")
    if content is None:
        source = ""
    else:
        source = content.text

    # extract the post's body
    paragraphs = soup.find_all(attrs={'class': 'ParagraphElement__ParagraphBase-sc-1soo3i3-0'})
    text = "\n".join(f"{p.text}" for p in paragraphs)

    return title, text, source, labels


def create_post(title: str, text: str, source: str, labels: list[str]) -> None:
    """
    Creates a news post with the given title, content, and source, and associates it with tags.

    Args:
        title (str): The title of the news post.
        text (str): The main content or body of the news post.
        source (str): The source of the news content.
        labels (list[str]): A list of labels (tags) to be associated with the news post.

    Returns:
        None
    """
    tags = []
    for label in labels:
        tag, created = Tag.objects.get_or_create(label=label.text)
        tags.append(tag)

    news, created = News.objects.get_or_create(
        title=title,
        content=text,
        source=source,
    )

    news.tags.set(tags)


def create_posts(urls: list[str]) -> None:
    """
    Creates multiple news posts in the database by extracting information from a list of URLs.

    Args:
        urls (list[str]): A list of URLs to process and create news posts from.

    Returns:
        None
    """
    for url in urls:
        post_content = extract_content(url)
        if post_content is None:
            print(f"no content found for {url}")
        else:
            create_post(*post_content)
