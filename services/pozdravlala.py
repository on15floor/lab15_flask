import requests
import json


def get_congratulation(reason=1, gender=0, l_c=2, polite=1, tr=0):
    """
        :param reason: Повод: 0 - Пожелание, 1 - День рожденья, 2 - 23.02, 3 - 8.03, 4 - Новый год, 5 - Рождество
        :param gender: Пол: 0 - Муж, 1 - Жен
        :param l_c: Длина: 0 - Короткое, 1 - Среднее, 2 - Длинное
        :param polite: Обращение: 0 - Ты, 1 - Вы
        :param tr: Транслит: 0 - Русские буквы, 1 - Транслит
        :return:
        """

    response = requests.post('http://www.pozdravlala.ru/gen',
                             data=f'[{reason},{gender},{l_c},{polite},{tr}]',
                             headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    res = json.loads(response.text)
    return res['text']
