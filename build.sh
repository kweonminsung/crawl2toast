rm -rf build dist *.spec


if [ $1 == "release" ]; then
    echo "Building for Release..."
    pyinstaller --onefile \
        --name "crawl2toast" \
        --clean \
        --noconfirm \
        --icon "public/icon.ico" \
        --add-data "public/*:public" \
        --add-data "locales/*:locales" \
        --add-binary "lib/crawler/chromedriver.exe:." \
        --noconsole \
        --optimize 2 \
        main.py
else
    echo "Building for Test..."
    pyinstaller --onefile \
        --name "crawl2toast" \
        --clean \
        --noconfirm \
        --icon "public/icon.ico" \
        --add-data "public/*:public" \
        --add-data "locales/*:locales" \
        --add-binary "lib/crawler/chromedriver.exe:." \
        main.py
fi

cp source.json dist