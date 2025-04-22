# crawl2toast

CSS 선택자를 이용해 웹에서 특정 정보를 주기적으로 수집하고, 실시간 윈도우 알림으로 알려주는 크롤링 도구(윈도우용)

| ~~테스트로 만든건데 하다보니 규모가 커짐~~

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
