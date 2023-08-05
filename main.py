from utils import get_hh_data, create_database, save_data_to_database
from config import config
from DBManager import DBManager


def main():
    employers_id = [
        '1740',  # Яндекс
        '80',  # Альфа-Банк
        '15478',  # vk
        '67611',  # Тензор
        '78638',  # Tinkoff
        '1057',  # kaspersky
        '3529',  # Сбер
        '3776',  # MTC
        '2180',  # OZON
        '4934'  # билайн
    ]
    params = config()

    print('Данная программа парсит информацию о 10 кампаниях и их вакансиях.\n'
          'Полученные данные записываются в базу данных "hh_ru" в таблицы "employers" и "vacancies"\n')
    input('Чтобы начать нажмите "Enter"\n')
    print('Идет сбор данных, это займет некоторое время.\n')

    data = get_hh_data(employers_id)
    print('Данные получены.')

    create_database('hh_ru', params)
    print('База данных создана.')

    save_data_to_database(data, 'hh_ru', params)
    print('Данные успешно перенесены в базу данных.')

    dbm = DBManager()

    while True:

        user_input = input('\nДля выбора действия введите соответствующее число:\n'
                           '  1 - Посмотреть список всех компаний и количество вакансий у каждой компании;\n'
                           '  2 - Посмотреть список всех вакансий(название компании, '
                           'название вакансии, зарплата, ссылка);\n'
                           '  3 - Посмотреть список компаний и среднюю зарплату по всем вакансиям от этой компании;\n'
                           '  4 - Посмотреть список всех вакансий, у которых зарплата выше средней по всем вакансиям;\n'
                           '  5 - Посмотреть список всех вакансий, в названии которых содержится ключевое слово;\n'
                           '  6 - Для выхода введите "exit".\n')

        if user_input.lower() == "exit":
            return

        elif user_input == '1':
            data = dbm.get_companies_and_vacancies_count()
            for row in data:
                print(row)

        elif user_input == '2':
            data = dbm.get_all_vacancies()
            for row in data:
                print(row)

        elif user_input == '3':
            data = dbm.get_avg_salary()
            for row in data:
                print(row)

        elif user_input == '4':
            data = dbm.get_vacancies_with_higher_salary()
            for row in data:
                print(row)

        elif user_input == '5':
            user_keyword = input("Введите ключевое слово:\n")
            data = dbm.get_vacancies_with_keyword(user_keyword)
            if data == list():
                print('К сожалению по данному критерию нет вакансий.')
            else:
                for row in data:
                    print(row)

        else:
            print('Не корректный ввод. Попробуйте снова.')


if __name__ == '__main__':
    main()
