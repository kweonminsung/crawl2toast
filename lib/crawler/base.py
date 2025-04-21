import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from lib.db import Database, create_history, get_histories, create_log
from lib.toaster import show_toast, show_compressed_toast
from lib.constants import USER_AGENT
from lib.settings import get_sources
from datetime import datetime

def get_html_by_selenium(url: str, wait: int) -> str:
    from lib.crawler import get_selenium_driver

    selenium_driver = get_selenium_driver()

    try:
        selenium_driver.get(url)
    except TimeoutException:
        raise Exception(f"TimeoutException: HTTP ({url})")
    
    selenium_driver.implicitly_wait(wait)
    
    return selenium_driver.page_source


def get_html_by_request(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": USER_AGENT})

    if response.status_code == 200:
        return response.text

    else:
        raise Exception(f"TimeoutException: HTTP {response.status_code}({url})")


def crawl():
    sources = get_sources()

    for _url, _source in sources.items():
        url_result = list()

        selector = _source["selector"]

        html = None

        try:
            if _source["options"]["render"]:
                wait = _source["options"]["render_wait"]
                html = get_html_by_selenium(_url, wait)
            else:
                html = get_html_by_request(_url)
                
            soup = BeautifulSoup(html, 'html.parser')

            try:
                parent_element = soup.select_one(selector["parent"])
            except Exception as e:
                raise Exception(f"ElementNotFoundException: {selector['parent']}({_url})")
            
            try:
                child_elements = parent_element.find_all(selector["child"], recursive=False)
            except Exception as e:
                raise Exception(f"ElementNotFoundException: {selector['parent']} > {selector['child']}({_url})")

            for child_element in child_elements:
                try:
                    content = str(child_element.select_one(selector["crawl_content"]).get_text()).strip()
                except Exception as e:
                    raise Exception(f"ElementNotFoundException: {selector['parent']} > {selector['child']} > {selector['crawl_content']}({_url})")

                link = None
                if selector["crawl_link"] is not None:
                    try:
                        link = str(child_element.select_one(selector["crawl_link"])["href"]).strip()
                    except Exception as e:
                        raise Exception(f"ElementNotFoundException: {selector['parent']} > {selector['child']} > {selector['crawl_link']}({_url})")

                url_result.append({
                    "content": content,
                    "link": link
                })

            if not _source["options"]["disable_history"]:
                last_history = get_histories(Database().get_connection(), _url, 1, 0)

                for result in url_result:
                    # Check if the content is already in the history
                    if _source["options"]["disable_last_history_check"] and len(last_history) > 0 and last_history[0]["content"] == result["content"]:
                        continue
                
                    create_history(Database().get_connection(), _url, result["content"])

            if len(url_result) > 0:
                show_compressed_toast(_source["name"], url_result[0]["content"], len(url_result) - 1)
            else:
                show_toast(_source["name"], url_result[0]["content"])


            
            create_log(Database().get_connection(), _url, True, "Crawled successfully")
            
            from lib.ui.settings_frame import set_recent_crawl
            set_recent_crawl(datetime.now())

            from lib.ui.main_frame import reload_current_history_listbox
            reload_current_history_listbox()

            from lib.ui.logs_frame import load_log_listbox
            load_log_listbox()
        except Exception as e:
            create_log(Database().get_connection(), _url, False, str(e))
            # print(f"Error occurred while crawling: {e}")
    
