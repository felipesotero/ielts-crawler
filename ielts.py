#!/usr/bin/env python
"""Script to check for availability of IELTS exams on a given country, city for a given module."""
import sys
import requests
from bs4 import BeautifulSoup

import options


# Default options:
TOWN = 'Recife'
MODULE = 2  # General Training
COUNTRY = 11  # Brazil

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/48.0.2564.82 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8'
}

FORM_URL = 'https://ielts.britishcouncil.org/Default.aspx'


def main(country=None, town=None, module=None):
    """Main entry point for the script."""
    # Prepare options
    country = country if country else COUNTRY
    town = town if town else TOWN
    module = module if module else MODULE

    # Instantiate the crawler and call all methods.
    crawler = IeltsCrawler(HEADERS, country, town, module)
    form_soup = crawler.get_country_form(FORM_URL)
    country_form_response_url = FORM_URL
    country_form_soup = crawler.fill_country_form_and_get_availability_form(form_soup, country_form_response_url)
    availability_result_page_soup = crawler.fill_availability_form_and_get_result_page(country_form_soup)
    return crawler.is_date_available(availability_result_page_soup)


class IeltsCrawler(object):
    def __init__(self, headers, country, town, module):
        # Prepare form request and form options
        self.country = country
        self.town = town
        self.module = module
        self.session = requests.Session()
        self.session.headers.update(headers)

    def get_country_form(self, form_url):
        # Get form
        country_form_response = self.session.get(form_url)
        # Parse response
        return BeautifulSoup(country_form_response.content, "html.parser")

    def fill_country_form_and_get_availability_form(self, form_soup, country_form_response_url):
        # Prepare to select Country
        VIEWSTATE = form_soup.find(id='__VIEWSTATE')['value']
        EVENTVALIDATION = form_soup.find(id='__EVENTVALIDATION')['value']

        form_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': VIEWSTATE,
            '__EVENTVALIDATION': EVENTVALIDATION,
            'ctl00$ContentPlaceHolder1$ddlCountry': self.country,
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
        VIEWSTATE = country_form_soup.find(id='__VIEWSTATE')['value']
        # EVENTVALIDATION = country_form_soup.find(id='__EVENTVALIDATION')['value']

        form_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': VIEWSTATE,
            'ctl00$ContentPlaceHolder1$ddlDateMonthYear': EARLY_DATE,
            'ctl00$ContentPlaceHolder1$ddlTownCityVenue': self.town,
            'ctl00$ContentPlaceHolder1$ddlModule': self.module,
            'ctl00$ContentPlaceHolder1$imgbSearch.x': 51,
            'ctl00$ContentPlaceHolder1$imgbSearch.y': 12
        }

        form_url = 'https://ielts.britishcouncil.org/CountryExamSearch.aspx'

        # Get Availability Form
        availability_form_response = self.session.post(form_url, data=form_data, headers={'Referer': form_url})
        # Parse response
        return BeautifulSoup(availability_form_response.content, "html.parser")

    '''Return a list of availabilities'''
    def get_availability_from_result_page(self, availability_soup):
        # Check if there's any availability:
        availabilities = []
        for exam in availability_soup.find_all('div', {'class': 'pnlBodyDetailRowBox'}):
            content = exam.find_all('div')[3].contents[0]
            availabilities.append('Full' not in content)

        return availabilities

    '''Return True if there is at least one date available'''
    def is_date_available(self, availability_soup):
        # Check if there's any availability:
        for exam in availability_soup.find_all('div', {'class': 'pnlBodyDetailRowBox'}):
            content = exam.find_all('div')[3].contents[0]
            if 'Full' not in content:
                return True
            return False


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 4:
        # Check if country, city and module is listed in constant options.
        country = args[1]
        city = args[2]
        module = args[3]

        # Check if values are in options.py constants:
        try:
            country = options.COUNTRIES[country]
            city = options.CITIES[city]
            module = options.MODULES[module]
        except:
            sys.exit('Country, City or Module option unavailable. Check spelling')
        sys.exit(0 if main(country, city, module) else 2)

    elif len(args) == 1:
        # Run with default options
        sys.exit(0 if main() else 2)
    else:
        sys.exit('You must provide the country, city and module in that order if you do not want\
            to run the default values, eg.: Brazil Recife "General Training"')
