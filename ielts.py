#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/48.0.2564.82 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8'
}

FORM_URL = 'https://ielts.britishcouncil.org/Default.aspx'


class IeltsCrawler(object):
    def __init__(self, headers):
        # Prepare form request
        self.session = requests.Session()
        self.session.headers.update(headers)

    def get_country_form(self, form_url):
        # Get form
        country_form_response = self.session.get(form_url)
        # Parse response
        return BeautifulSoup(country_form_response.content, "html.parser")

    def fill_country_form_and_get_availability_form(self, form_soup, country_form_response_url):
        # Prepare to select Brazil
        BRAZIL = 11
        VIEWSTATE = form_soup.find(id='__VIEWSTATE')['value']
        EVENTVALIDATION = form_soup.find(id='__EVENTVALIDATION')['value']

        form_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': VIEWSTATE,
            '__EVENTVALIDATION': EVENTVALIDATION,
            'ctl00$ContentPlaceHolder1$ddlCountry': BRAZIL,
            'ctl00$ContentPlaceHolder1$imgbRegisterBtn.x': 59,
            'ctl00$ContentPlaceHolder1$imgbRegisterBtn.y': 8
        }

        brazil_form_response = self.session.post(
            country_form_response_url, data=form_data, headers={'Referer': country_form_response_url}
        )
        # Parse response
        return BeautifulSoup(brazil_form_response.content, "html.parser")

    def fill_availability_form_and_get_result_page(self, country_form_soup):
        # Prepare to select the month, city and module:
        EARLY_DATE = country_form_soup.find(id='ctl00_ContentPlaceHolder1_ddlDateMonthYear').find('option')['value']
        TOWN = 'Recife'
        MODULE = 2  # General Training
        VIEWSTATE = country_form_soup.find(id='__VIEWSTATE')['value']
        # EVENTVALIDATION = country_form_soup.find(id='__EVENTVALIDATION')['value']

        form_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': VIEWSTATE,
            'ctl00$ContentPlaceHolder1$ddlDateMonthYear': EARLY_DATE,
            'ctl00$ContentPlaceHolder1$ddlTownCityVenue': TOWN,
            'ctl00$ContentPlaceHolder1$ddlModule': MODULE,
            'ctl00$ContentPlaceHolder1$imgbSearch.x': 51,
            'ctl00$ContentPlaceHolder1$imgbSearch.y': 12
        }

        form_url = 'https://ielts.britishcouncil.org/CountryExamSearch.aspx'

        # Get Availability Form
        availability_form_response = self.session.post(form_url, data=form_data, headers={'Referer': form_url})
        # Parse response
        return BeautifulSoup(availability_form_response.content, "html.parser")

    def get_availability_from_result_page(self, availability_soup):
        # Check if there's any availability:
        availabilities = []
        for exam in availability_soup.find_all('div', {'class': 'pnlBodyDetailRowBox'}):
            content = exam.find_all('div')[3].contents[0]
            availabilities.append('Full' not in content)

        return str(availabilities)


# Instantiate the crawler and call all methods.
crawler = IeltsCrawler(HEADERS)
form_soup = crawler.get_country_form(FORM_URL)
country_form_response_url = FORM_URL
country_form_soup = crawler.fill_country_form_and_get_availability_form(form_soup, country_form_response_url)
availability_result_page_soup = crawler.fill_availability_form_and_get_result_page(country_form_soup)
print crawler.get_availability_from_result_page(availability_result_page_soup)

# TODO: Parametrize the options (country, town, module)
