import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from lib.settings import get_settings

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

selenium_driver = None

def initialize_selenium_driver():
    global selenium_driver

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"user-agent={USER_AGENT}")

    selenium_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def terminate_selenium_driver():
    global selenium_driver

    if selenium_driver is not None:
        selenium_driver.quit()
        selenium_driver = None
    

def get_html_by_selenium(url: str, wait: int) -> str:
    try:
        selenium_driver.get(url)
    except TimeoutException:
        raise Exception("Timeout while loading the page.")
    
    selenium_driver.implicitly_wait(wait)
    
    return selenium_driver.page_source


def get_html_by_request(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": USER_AGENT})

    if response.status_code == 200:
        return response.text

    else:
        raise Exception(f"Failed to retrieve the page. Status code: {response.status_code}")


def crawl() -> dict[str, list[dict[str, str | None]]]:
    settings = get_settings()
    
    result = dict()

    for source in settings["source"]:
        url_result = list()

        url = source["url"]
        selector = source["selector"]

        html = None

        if source["render_options"]["render"]:
            wait = source["render_options"]["wait"]
            html = get_html_by_selenium(url, wait)
        else:
            html = get_html_by_request(url)
            
        soup = BeautifulSoup(html, 'html.parser')
        parent_element = soup.select_one(selector["parent"])

        for child_element in parent_element.find_all(selector["child"], recursive=False):
            print(child_element)
            print(child_element.select_one(selector["crawl_title"]).text)

            title = str(child_element.select_one(selector["crawl_title"]).text).strip()

            content = None
            if selector["crawl_title"] is not None:
                content = str(child_element.select_one(selector["crawl_content"]).text).strip()

            link = None
            if selector["crawl_link"] is not None:
                link = str(child_element.select_one(selector["crawl_link"])["href"]).strip()

            url_result.append({
                "title": title,
                "content": content,
                "link": link
            })

        result[url] = url_result

    return result