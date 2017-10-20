import sys
sys.path.append("/home/woo/git_repos/expediascraperoneway")
import requests
from lxml import html
import time


def checkingForNonEmptyList(url):
    testingValue = 1
    json_data_xpath = []

    while (testingValue == 1):
        print(url)
        response = requests.get(url)
        parser = html.fromstring(response.text)
        json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")

        lenghtOfjson_data_xpath = len(json_data_xpath)

        if not lenghtOfjson_data_xpath:
            testingValue = 1
            waitTenSeconds()
            print ("List is Empty")
        else:
            testingValue = 0
            print ("List is NOt Empty")

    return json_data_xpath

def waitTenSeconds():
    time.sleep(15)