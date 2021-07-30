import asyncio
import re
import validators
import csv
from pyppeteer import launch
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

# Define the list of URLs you want to scrape
urls = [
'https://www.zendesk.com', 
'https://stackoverflow.com',
'https://google.com',
'https://aennisjr.com'
]

emails = []

async def close_dialog(dialog):
    print("Dialog Dismissed: ")
    await dialog.accept()

async def main():

    count = 1

    with open('email_addresses.csv', 'w') as file:

        w = csv.writer(file)
        w.writerow(['website', 'email'])
        # Launch a new browser window
        browser = await launch({ 'headless': True })

        for u in urls:

            skip = 0

            print("Scraping: " + str(u) + " - [" + str(count) + "/" + str(len(urls)) + "]")
            
            if validators.url(str(u)):
                # Open a new tab in the browser 
                # - wait until network idle status is achieved (all content loaded)
                page = await browser.newPage()

                # set action to be completed when a prompt is encountered
                page.on('dialog', lambda dialog: asyncio.ensure_future(close_dialog(dialog)))

                try:
                    await page.goto(u, {'waitUntil': 'networkidle2', 'timeout': 60000})
                except:
                    print("ERROR: Couldn't navigate to " + str(u))
                    skip = 1

                if skip == 0:
                    # Capture all body content
                    content = await page.evaluate('document.body.innerHTML')
                    # Grab emails from the page
                    found_emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(content).lower())

                    if found_emails: # store found email addresses in emails list
                        for f in found_emails:
                            print(f)
                            emails.append(f)
                            w.writerow([u, f])
                    else:
                        print("No emails found on " + str(u))

                    soup = BeautifulSoup(content, 'html.parser')
                    found_urls = soup.find_all('a', href=True)
                    sub_traversed = []

                    if found_urls:
                        for link in found_urls:

                            domain = urlparse(str(u)).netloc

                            goto_url = link['href']
                            
                            if str(link['href']).startswith('/'):
                                goto_url = 'https://' + str(domain) + str(link['href'])
                            
                            # if the emails contains the base domain, is not in the list of traversed emails, and is a valid url
                            if domain in goto_url and str(goto_url) not in sub_traversed and validators.url(str(goto_url)):
                                
                                try:
                                    print("sub url: " + goto_url)

                                    await page.goto(str(goto_url), {'waitUntil': 'networkidle2', 'timeout': 35000})

                                    content = await page.evaluate('document.body.innerHTML')
                                    found_emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(content).lower())
                                    
                                    # add this sub url to list of urls already traversed
                                    sub_traversed.append(str(goto_url))
                                    
                                    if found_emails: # store found email addresses in emails list
                                        for f in found_emails:
                                            print(f)
                                            emails.append(f)
                                            w.writerow([u, f])

                                    else:
                                        print("No emails found on " + str(goto_url))

                                except:
                                    print("ERROR: Couldn't navigate to subpage: " + str(goto_url))
                                finally:
                                    continue
            else:
                print("Invalid URL " + str(u))

            # Close browser window
            await page.close()

            count += 1

        if not emails:
            print('Process complete. No email addresses found.')
        else:
            print('Process complete. ' + str(len(emails)) + ' items found.')
    
asyncio.get_event_loop().run_until_complete(main())