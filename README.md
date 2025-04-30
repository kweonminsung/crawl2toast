# crawl2toast

<img src="https://github.com/kweonminsung/crawl2toast/blob/main/public/icon.png" />

Real-time toast notification of crawled data with CSS selectors(Windows Only)

### Download

You can download the executable file from the [release tab](https://github.com/kweonminsung/crawl2toast/releases).

### Prerequisites

- Windows 10 or over
- [Chome Browser](https://www.google.com/intl/ko_kr/chrome/)

### Developed with

- [python 3.12](https://www.python.org/)
- [tkinter](https://docs.python.org/3/library/tkinter.html) | [pyinstaller](https://www.pyinstaller.org/)
- SQLite3
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) | [Selenium](https://www.selenium.dev/)
- [ChromeDriver 135](https://developer.chrome.com/docs/chromedriver/get-started)

### Get Started (CMD)

```cmd
git clone https://github.com/kweonminsung/crawl2toast.git

python -m venv venv

venv\Scripts\activate.bat

pip install -r requirements.txt

python main.py
```

### Build (CMD)

```cmd
venv\Scripts\activate.bat

<!-- Release Build -->
build.bat release

<!-- Test Build -->
build.bat
```
