"""
В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель и ученик смогли
объяснить нашей поддержке, кого они имеют в виду ( у преподавателей, например, часто учится несколько Саш),
мы генерируем пользователям уникальные и легко произносимые имена. Имя у нас состоит из прилогательного,
имени животного и двузначной цифры. В итоге получается, например, "Перламутровый лось 77".
Для генерации таких имен мы и решали следующую задачу:
Получить с русской википедии список всех животных (url: ) и ввести количество животных на каждую букву алфавита.
Результат должен получиться в следующем виде:
А: 642

"""
import re
import requests
from bs4 import BeautifulSoup

URL = [
    "https://ru.m.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%D0%90"]
HOST = "https://ru.wikipedia.org"  # нужен изменяймый тип данных
HEADERS = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (HTML, like Gecko) "
                  "Version/13.0.3 Mobile/15E148 Safari/604.1", "accept": "*/*"}
animals_dict = {}  # словарь животных
alphabet = [chr(i) for i in range(1040, 1046)] + [chr(1025)] + [chr(j) for j in range(1046, 1072)]  # генерируем алфавит
for i in alphabet:  # заполним словарь ключами русского алфавита
    animals_dict[i] = 0
count = 0  # количество страниц необходимое для цикла функции get_content


def get_html(url, params=None):
    """
    :param url: Передаем нужны url
    :param params: если есть пагинация
    :return:
    """
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def parse_count_page(html):
    """
    Функция подсчета количества страниц которые будут обработанны и результаты записанны в animals_dict
    :param html:
    :return: количество страниц необходимое для цикла функции get_content
    """
    soup = BeautifulSoup(html, "html.parser")
    count_page = soup.find("div", id="mw-pages").find("p").get_text()  # показывает количество страниц
    count_page = re.findall("(\d+)", count_page)  # получаем список цифр, 0 индекс - количество животных на странице
    # 1-2 индекс общее количество животных
    count_animals = int(count_page[0])  # приводим строку к числу
    all_animals = int(count_page[1] + count_page[2])  # приводим строку к числу
    count = all_animals // count_animals  # вычисляем количество страниц необходимое для цикла функции get_content
    return count


def get_content(html):
    """
    Парсит получаемый текст страницы библиотекой BeautifulSoup
    :param html:
            URL: ссылка на страницу которую будет парсить функция список со строковым одним значением
    :return: получаем словарь с ключами по русскому алфавиту и со значениями количесва животных,а так же новый URL
    """

    soup = BeautifulSoup(html, "html.parser")
    items = soup.find("div", class_="mw-category")  # по тегу "div" получаем  строки нужного класса
    tmp = []  # временный лист в который добавим строку с животными
    for i in items:
        tmp.append(i.find("ul").get_text())  # по тегу ul для каждой группы животных  получаем текст
    animal_list = []
    for i in range(len(tmp)):  # циклом убираем красные строки и разделим настроки
        animal_list += tmp[i].split("\n")

    str_link_first_page = soup.find("div", id="mw-pages").find("a")  # для первой странице " следующая" для второй иначе
    str_link_next_page = soup.find("div", id="mw-pages").find("a").find_next()  # для второй странице "следующая стр"

    link_next_page = HOST + str_link_first_page.get("href")  # ссылка на вторую страинцу списка животных

    for i in alphabet:  # двумя цыклами считаем и увеличиваем значения в ключах словаря
        for j in animal_list:
            if j[0] == i:
                animals_dict[i] += 1

    if URL == link_next_page:
        return print("Парсинг закончился")
    elif str_link_next_page.get("href") == None:
        URL[0] = link_next_page
    else:
        URL[0] = HOST + str_link_next_page.get("href") # для первой страницы - это пустая последовательность

    return animals_dict


def parse():
    URL_str = URL[0]  # получаем строку URL
    html = get_html(URL_str)
    count = parse_count_page(html.text)  # счетчик страниц для парсинга
    if html.status_code == 200:
        for i in range(0, count + 1):
            get_content(html.text)
            URL_str = URL[0]
            html = get_html(URL_str)
    else:
        print("Error")


if __name__ == '__main__':
    parse()
    print(animals_dict)
