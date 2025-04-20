import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from lib.db import Database, create_history, get_histories
from lib.toaster import show_toast, show_compressed_toast
from lib.constants import USER_AGENT
from lib.settings import get_sources

def get_html_by_selenium(url: str, wait: int) -> str:
    from lib.crawler import get_selenium_driver

    selenium_driver = get_selenium_driver()

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


def _crawl() -> dict[str, list[dict[str, str | None]]]:
    sources = get_sources()
    
    result = dict()

    for _url, _source in sources.items():
        url_result = list()

        selector = _source["selector"]

        html = None

        if _source["options"]["render"]:
            wait = _source["options"]["render_wait"]
            html = get_html_by_selenium(_url, wait)
        else:
            html = get_html_by_request(_url)
            
        soup = BeautifulSoup(html, 'html.parser')
        parent_element = soup.select_one(selector["parent"])

        for child_element in parent_element.find_all(selector["child"], recursive=False):
            # print(child_element.select_one(selector["crawl_title"]).text)

            content = str(child_element.select_one(selector["crawl_content"]).text).strip()

            link = None
            if selector["crawl_link"] is not None:
                link = str(child_element.select_one(selector["crawl_link"])["href"]).strip()

            url_result.append({
                "content": content,
                "link": link
            })

        result[_url] = url_result

    return result


def crawl():
    sources = get_sources()
    results = _crawl()

    for _url, _source in sources.items():
        if not _source["options"]["disable_history"]:
            for result in results[_url]:
                if _source["options"]["disable_last_history_check"]:
                    continue

                last_history = get_histories(Database().get_connection(), _url, 1, 0)

                # Check if the content is already in the history
                if len(last_history) > 0 and last_history[0]["content"] == result["content"]:
                    continue
            
                create_history(Database().get_connection(), _url, result["content"])

        if len(results[_url]) > 0:
            show_compressed_toast(_source["name"], results[_url][0]["content"], len(results[_url]) - 1)
        else:
            show_toast(_source["name"], results[_url][0]["content"])