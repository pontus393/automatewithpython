#! python3
# autoUnsubscriber.py
# Finds unsubscribe links in your email and opens them

import imapclient
import pyzmail
import bs4
import re
import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Establish connection and finding emails
server = imapclient.IMAPClient('<INSERT IMAP>, ssl=True)
server.login('<INSERT EMAIL ADDRESS>', input('Enter password > '))
server.select_folder('INBOX', readonly=True)
UIDs = server.search(['BODY', 'unsubscribe']) # finds email containing str "unsubscribe"
rawMessages = server.fetch(UIDs, ['BODY[]'])

# Reading emails and saving unsubscribe links
links = []
for UID in UIDs:
    message = pyzmail.PyzMessage.factory(rawMessages[UID][b'BODY[]'])
    if message.html_part != None:
        body = message.html_part.get_payload().decode(message.html_part.charset)
        # bs4, spara länken till en lista.
        soup = bs4.BeautifulSoup(body, 'html.parser')
        if soup.find("a", string=re.compile("unsubscribe", re.IGNORECASE)) != None:
            links.append(soup.find("a", string=re.compile("unsubscribe", re.IGNORECASE)).get("href"))

print("Found %s links:" % (len(links)))
pprint.pprint(links)
print("Press enter to open links.")
input()

browser = webdriver.Firefox()
for link in links:
    browser.get(link)
    input('Press enter to open next link.')
