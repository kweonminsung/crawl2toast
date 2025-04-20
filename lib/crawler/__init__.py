import threading
import queue
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from lib.constants import USER_AGENT, SELUMIUM_DRIVER_TERMINATE_WAIT
# from lib.settings import get_sources
from lib.crawler.base import crawl

task_queue = queue.Queue()

selenium_driver: webdriver.Chrome | None = None

# Create crawler queue thread
def initialize():
    thread = threading.Thread(target=crawler_thread, daemon=True)
    thread.start()
    return thread


def crawler_thread():
    global selenium_driver

    # Initialize the Selenium driver if any source requires rendering
    # sources = get_sources()
    # need_renderer = False
    # for _url, _source in sources.items():
    #     if _source["options"]["render"] == True:
    #         need_renderer = True
    #         break
    # if need_renderer:
    #     initialize_selenium_driver()

    # Start the task queue
    while True:
        try:
            task = task_queue.get(timeout=SELUMIUM_DRIVER_TERMINATE_WAIT)
        except queue.Empty:
            # If the task queue is empty and the Selenium driver is not None, terminate the driver
            if selenium_driver is not None:
                print("No tasks remaining. Terminating Selenium driver.")
                terminate_selenium_driver()
            continue

        if task is None:
            print("Crawler thread shutting down.")
            break

        print("Crawler thread received a task.")
        crawl()
        print("Crawler task completed.")

        task_queue.task_done()

    # Terminate the Selenium driver if crawler thread is shutting down
    terminate_selenium_driver()


def request_crawl():
    task_queue.put("crawl")
    print("Crawl task requested.")


def terminate_crawler_thread():
    task_queue.put(None)
    task_queue.join() 


def initialize_selenium_driver():
    global selenium_driver

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-usb-keyboard-detect')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument(f"user-agent={USER_AGENT}")
    
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    selenium_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def get_selenium_driver() -> webdriver.Chrome:
    global selenium_driver

    if selenium_driver is None:
        initialize_selenium_driver()

    return selenium_driver


def terminate_selenium_driver():
    global selenium_driver

    if selenium_driver is not None:
        selenium_driver.quit()
        selenium_driver = None