# web-scraping
A collection of scripts for web scraping.

## email_scraper.py
Can be used to collect email addresses from any webpage. You can do this by defining a list of URLs and then running the script. The output is saved in CSV format by default.
Dependencies:
- asyncio - asyncio is a library to write concurrent code using the async/await syntax.
- pyppeteer - unofficial Python port of puppeteer JavaScript (headless) chrome/chromium browser automation library.
- pandas - data analysis and manipulation tool
- validators - data validation library

pyppeteer requires Python >= 3.6. Install with pip from PyPI:

```pip install pyppeteer```

Or install the latest version from this github repo:

```pip install -U git+https://github.com/pyppeteer/pyppeteer@dev```

pandas can be installed via pip from PyPI. Requires Python 3.7.1 and above.

```pip install pandas```

You can install validators using pip. Supports python versions 2.7, 3.3, 3.4, 3.5 and PyPy:

```pip install validators```

Notes:

`df.to_csv('email_addresses.csv', index=False)` - saves your data in a CSV file called "email_addresses.csv". You can use other methods such as `to_html` `to_json` `to_excel` etc. in order to save it in other formats. You can find a reference to this and other methods here: [Pandas API](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html)

## traversive_email_scraper.py
Can be used to traverse several pages of a website in order to collect email addresses. Much like email_scraper.py, just define a list of URLs then execute the program in order to start the crawling process.
