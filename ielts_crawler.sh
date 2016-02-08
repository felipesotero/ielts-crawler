#!/bin/bash
source /home/web/.virtualenvs/crawler/bin/activate
sleep 1
cd /home/web/webapps/ielts-crawler
python main.py >> /home/web/webapps/ielts-crawler/log.log
sleep 5
deactivate