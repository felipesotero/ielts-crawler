#!/usr/bin/env python
"""
Main execution of the program.
Check if there's available spots for takign the IELTS exams and send an email with info.
"""
import sys
from datetime import datetime

import ielts
import notice_email
import options


def send_email():
    new_email = notice_email.NoticeEmail('luizsotero@gmail.com')
    new_email.send_message('IELTS now available!',
                           'Check https://ielts.britishcouncil.org for the availability immediately.')

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
            if ielts.main(country, city, module):
                # Send email
                send_email()
            else:
                print 'No availability at ' + str(datetime.utcnow())
            sys.exit(0)

    elif len(args) == 1:
        # Run with default options
        if ielts.main():
            send_email()
            print 'Availability found! ' + str(datetime.utcnow())
        else:
            print 'No availability at ' + str(datetime.utcnow())
        sys.exit(0)
    else:
        sys.exit('You must provide the country, city and module in that order if you do not want\
            to run the default values, eg.: Brazil Recife "General Training"')
