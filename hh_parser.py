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
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'}

base_url = 'https://hh.ru/search/vacancy?search_period=3&clusters=true&area=1002&text=python&enable_snippets=true'


def parse_hh(base_url, headers):
    jobs = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('OK!')
        soup = bs(request.content, 'html.parser')
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
        print(jobs)
    else:
        print('Error!!!')


parse_hh(base_url, headers)
