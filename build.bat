rmdir /s /q build
rmdir /s /q dist
del *.spec

if "%1"=="release" (
    echo Building for Release...
    pyinstaller --onefile ^
        --name "crawl2toast" ^
        --clean ^
        --noconfirm ^
        --icon "public/icon.ico" ^
        --add-data "public/*;public" ^
        --add-data "locales/*;locales" ^
        --add-binary "lib/crawler/chromedriver.exe;." ^
        --noconsole ^
        --optimize 2 ^
        main.py
) else (
    echo Building for Test...
    pyinstaller --onefile ^
        --name "crawl2toast" ^
        --clean ^
        --noconfirm ^
        --icon "public/icon.ico" ^
        --add-data "public/*;public" ^
        --add-data "locales/*;locales" ^
        --add-binary "lib/crawler/chromedriver.exe;." ^
        main.py
)

if exist source.json (
    copy source.json dist\
)