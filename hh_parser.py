# ------------------------------------------------------
#
# Program by Eugene Koleda
#
#
#
# Version       Date        Info
# 1.0           2019    Initial Version
#
# ------------------------------------------------------

import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'}

base_url = 'https://hh.ru/search/vacancy?search_period=3&clusters=true&area=1002&text=python&enable_snippets=true&page=0'


def export_to_csv(jobs):
    with open('parsed_jobs.csv', 'w', encoding='utf-8') as f:
        a_pen = csv.writer(f)
        a_pen.writerow(('Title', 'URL', 'Company', 'Description'))

        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['description']))


def parse_hh(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('OK!')
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?search_period=3&clusters=true&area=1002&text=python&enable_snippets=true&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            for div in divs:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                responsibility = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})
                requirements = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})
                content = f'{responsibility.text} {requirements.text}'
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'description': content
                })
        for job in jobs:
            print(job)
    else:
        print('Error!!!')
    export_to_csv(jobs)


parse_hh(base_url, headers)
