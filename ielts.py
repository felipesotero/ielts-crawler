#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup


form_url = 'https://ielts.britishcouncil.org/Default.aspx'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/48.0.2564.82 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8'
}

# Prepare form request
session = requests.Session()
session.headers.update(headers)
# Get form
country_form_response = session.get(form_url)
# Parse response
form_soup = BeautifulSoup(country_form_response.content, "html.parser")

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


brazil_form_response = session.post(form_url, data=form_data, headers={'Referer': country_form_response.url})
# Parse response
brazil_form_soup = BeautifulSoup(brazil_form_response.content, "html.parser")

# ----- Second part ------
# Chose city, date and module

# Prepare to select the month, city and module:
EARLY_DATE = brazil_form_soup.find(id='ctl00_ContentPlaceHolder1_ddlDateMonthYear').find('option')['value']
TOWN = 'Belo Horizonte'
MODULE = 2  # General Training
VIEWSTATE = brazil_form_soup.find(id='__VIEWSTATE')['value']
# EVENTVALIDATION = brazil_form_soup.find(id='__EVENTVALIDATION')['value']

form_data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': VIEWSTATE,
    # '__EVENTVALIDATION': EVENTVALIDATION,
    'ctl00$ContentPlaceHolder1$ddlDateMonthYear': EARLY_DATE,
    'ctl00$ContentPlaceHolder1$ddlTownCityVenue': TOWN,
    'ctl00$ContentPlaceHolder1$ddlModule': MODULE,
    'ctl00$ContentPlaceHolder1$imgbSearch.x': 51,
    'ctl00$ContentPlaceHolder1$imgbSearch.y': 12
}

form_url = 'https://ielts.britishcouncil.org/CountryExamSearch.aspx'

# Get Availability Form
availability_form_response = session.post(form_url, data=form_data, headers={'Referer': form_url})
# Parse response
availability_soup = BeautifulSoup(availability_form_response.content, "html.parser")

# ----- Third part ------
# Get availability and take action

# Check if there's any availability:
availabilities = []
for exam in availability_soup.find_all('div', {'class': 'pnlBodyDetailRowBox'}):
    content = exam.find_all('div')[3].contents[0]
    availabilities.append('Full' not in content)

# Take actions:
print availability_form_response.url
print availability_form_response.content
print str(availabilities)
