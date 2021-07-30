import asyncio
import re
import validators
import sys
from pyppeteer import launch
from pandas import DataFrame

# Define the list of URLs you want to scrape
urls = [
'https://www.zendesk.com/contact/', 
'https://stackoverflow.com/company/contact',
'https://google.com',
'https://aennisjr.com/contact/'
]

emails = []

async def main():
    # Launch a new browser window
    browser = await launch()

    # Loop through the URLs in the list
    for u in urls:
        
        if validators.url(str(u)):
            # Open a new tab in the browser 
            # - wait until network idle status is achieved (all content loaded)
            page = await browser.newPage()
            await page.goto(u, {'waitUntil': 'networkidle2'})

            # Capture all body content
            content = await page.evaluate('document.body.innerHTML')

            # Grab emails from the page
            found = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(content).lower())

            if found: # store found email addresses in emails list
                for f in found:
                    print(f)
                    emails.append(f)
            else:
                print("No emails found on " + str(u))
            
            # Close browser window
            await page.close()
        else:
            print("Invalid URL " + str(u))

    # Close browser
    await browser.close()

    if emails:
        # Display captured email addresses
        print(emails)

        # Convert list to dataframe
        df = DataFrame (emails, columns=['email_addresses'])

        # Drop duplicate entries
        df.drop_duplicates(subset='email_addresses', keep="last", inplace=True)
        
        # Save to CSV
        df.to_csv('email_addresses.csv', index=False)
    else:
        print('Process complete. No email addresses found.')
    
asyncio.get_event_loop().run_until_complete(main())