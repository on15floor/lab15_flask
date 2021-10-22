import requests
from bs4 import BeautifulSoup


def beget_news_pars() -> list:
    """ Функция получает список новостей с beget.com
    :return: Список новостей
    """
    response = requests.get("https://beget.com/ru/news/2021/beget-12-years")
    soup = BeautifulSoup(response.text, 'html.parser')
    beget_news = soup.find_all("ul", {"class": "nav nav-category-tree flex-nowrap my-0"})
    res = []
    for n in beget_news[0].contents:
        res.append(n.text.strip())
    return res


def app_time_pars() -> list:
    """ Функция получает список скидок на игры для ios
    :return: Список словарей с информацией по играм
    """
    response = requests.get("https://app-time.ru/skidki-rasprodazhi-izmeneniya-novinki-appstore")
    soup = BeautifulSoup(response.text, 'html.parser')
    app_time_news = soup.find_all("div", {"class": "item-sales"})
    res = []
    for game in app_time_news:
        res.append({
            'game_name': game.contents[1].contents[0].text,
            'price_old': game.contents[1].contents[3].text,
            'price_new': game.contents[1].contents[2].text,
            'sale_percent': game.contents[0].contents[0].text,
            'cover': game.contents[0].contents[1].attrs['src'],
            'app_link': game.contents[2].attrs['href'].split('?at')[0],
        })
    return res
