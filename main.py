import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import re

def get_html():
    """
    Makes scrapping of web-page and returns html-code as text
    return: response (str) - html code of page
    """
    
    results = []
    url = 'https://jobs.dou.ua/companies/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.106 Safari/537.36 '
    }

    client = requests.session()
    first_part = client.get(url, headers=headers)

    soup = BeautifulSoup(first_part.text, features="html.parser")  # создаю объект-парсер для проверки

    # наличия кнопки и результатов на странице
    if soup.find('ul', {'class': 'l-items'}) is None:  # если на странице нет списка результатов
        response = None

    elif soup.find('div', {'class': 'more-btn'}) is None:  # если на странице нет кнопки "Больше компаний"
        response = first_part

    # парсим первую страницу
    items = soup.findAll('li', {'class': 'l-company'})
    for item in items:
        company = item.find('div', {'class': 'h2'}).find('a').text
        link = item.find('div', {'class': 'h2'}).find('a').get('href')
        results.append((company, link))
        print(company, link)


    else:  # если есть список вакансий и есть кнопка "Больше вакансий"


        pattern = 'https://jobs.dou.ua/companies/xhr-load/?'

        csrf = dict(client.cookies)['csrftoken']  # сохраняем токен
        headers['Referer'] = url  # дополняет хидеры для пост-запроса
        data = dict(csrfmiddlewaretoken=csrf, count=20)  # данные, которые передаём пост-запросом

        while True:
            second_part = client.post(pattern, headers=headers, data=data)

            soup = BeautifulSoup(second_part.json()['html'], features="html.parser")
            items = soup.findAll('a', {'class': 'cn-a'})

            count = 0
            for item in items:
                company = item.text
                link = item.get('href')
                results.append((company, link))
                count += 1

                print(company, link)
            data['count'] = data['count'] + count
            if second_part.json()['last']:  # когда у полученных данных флаг, что они последние
                break
        response = result

    client.close()
    return response


def main():
    get_html()


if __name__ == '__main__':
    main()