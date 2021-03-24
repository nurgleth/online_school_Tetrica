"""
Мы сохраняем время присутствия каждого пользователя на уроке в виде интервалов. В функцию передается словарь,
содержащий три списка с таймстепами (время в секундах):
-lesson - начало и конец урока
-pupil - интервалы присутствия ученика
-tutor - интервалы присутствия учителя
Интервалы устроены слудующим образом - это всегда список из четного количества элементов.
Под четными индексами (начиная с 0) время входа на урок, под нечетными - время выхода с урока.
нужно написать функцию, которая получает на вход словар с интервалами и возвращает время общего присутствия ученика и
учителя на уроке (в секундах). Будет плюсом: написать WEB API  с единственным endpoint'ом для вызова этой функции.
"""


def appearance(intervals: dict):
    """
    функция принимает словарь со значениями ключей в виде списка интервала времени
    :param intervals: ключи str, значания list
    :return: сумма общего время присуствия в секундах для каждого ключа
    """
    lesson = []  # создаем список времени в секундах для урока
    start_lesson = intervals["lesson"][0]
    stop_lesson = intervals["lesson"][1]
    tmp = (i for i in range(start_lesson + 1, stop_lesson + 1))  # генерируем секунды и добавляем их в список
    for i in tmp:
        lesson.append(i)
    lesson.sort()  # на всякий случай отсортируем список если временные промежутки были данны в разнобой
    lesson_set = set()  # создаем можество для временых промежутков урока
    lesson_set.update(lesson)  # добавляем во множество список элемнтов

    pupil = []  # создаем список времени в секундах для ученика
    start_all_pupil = intervals["pupil"][::2]
    stop_all_pupil = intervals["pupil"][1::2]
    for i in range(len(start_all_pupil)):  # генерируем секунды и добавляем их в список
        tmp = (i for i in range(start_all_pupil[i] + 1, stop_all_pupil[i] + 1))
        for i in tmp:
            pupil.append(i)
    pupil.sort()
    pupil_set = set()  # создаем можество для временых промежутков ученика
    pupil_set.update(pupil)  # добавляем во множество список элемнтов

    tutor = []  # создаем список времени в секундах для учителя
    start_all_tutor = intervals["tutor"][::2]

    stop_all_tutor = intervals["tutor"][1::2]
    for i in range(len(start_all_tutor)):  # генерируем секунды и добавляем их в список
        tmp = (i for i in range(start_all_tutor[i] + 1, stop_all_tutor[i] + 1))
        for i in tmp:
            tutor.append(i)
    tutor.sort()
    tutor_set = set()  # создаем можество для временых промежутков учителя
    tutor_set.update(tutor)  # добавляем во множество список элемнтов

    all_time = []  # список в секундах времени общего присутствия ученика и учителя
    all_time_set = lesson_set & tutor_set & pupil_set  # пересечение множеств дает нам общее время присутствия
    for i in all_time_set:
        all_time.append(i)
    return len(all_time)  # длина списка - общее время присутствия


tests = [{"data": {"lesson": [1594663200, 1594666800],
                   "pupil": [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   "tutor": [1594663290, 1594663430, 1594663443, 1594666473]},
          "answer": 3117},
         {"data": {"lesson": [1594702800, 1594706400],
                   "pupil": [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513,
                             1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009,
                             1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773,
                             1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                             1594706524, 1594706524, 1594706579, 1594706641],
                   "tutor": [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
          "answer": 3577},
         {"data": {"lesson": [1594692000, 1594695600],
                   "pupil": [1594692033, 1594696347],
                   "tutor": [1594692017, 1594692066, 1594692068, 1594696341]},
          "answer": 3565},
         ]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test["data"])
        assert test_answer == test["answer"], f"Error on test case {i}, got {test_answer}, expected{test['answer']}"
