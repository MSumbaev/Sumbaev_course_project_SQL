import requests
import json


def get_hh_data(employers_id: list):
    """Получение данных о работадателях и вакансиях с помощью API hh.ru"""
    data = []

    employers_data = []
    for employer_id in employers_id:

        response_emp = requests.get(f'https://api.hh.ru/employers/{employer_id}')

        employer_data = response_emp.json()
        employers_data.append(employer_data)

        vacancies_data = []
        count_page = (int(employer_data['open_vacancies']) // 100) + 1
        # Ограничение API на получение больше 2000 вакансий
        if count_page > 20:
            count_page = 20

        for page in range(count_page):
            params = {
                "employer_id": employer_id,
                "per_page": 100,
                "page": page,
                "area": 113
            }

            response_vac = requests.get(f'https://api.hh.ru/vacancies', params=params)
            vacancy_data = response_vac.json()
            formatted_vacancies = format_vacancies(vacancy_data['items'])
            vacancies_data.extend(formatted_vacancies)

        data.append({
            'employer': employers_data[0],
            'vacancies': vacancies_data
        })

    return data


def format_vacancies(vacancies: list):
    """Форматирование данных о вакансиях"""
    formatted_vacancies = []

    for v in vacancies:
        formatted_v = dict()
        formatted_v['name'] = v['name']

        if v['salary'] is None:
            formatted_v['salary_from'] = None
            formatted_v['salary_to'] = None
            formatted_v['currency'] = None
        else:
            formatted_v['salary_from'] = v['salary']['from']
            formatted_v['salary_to'] = v['salary']['to']
            formatted_v['currency'] = v['salary']['currency']

        formatted_v['city'] = None if v['address'] is None else v['address']['city']
        formatted_v['url'] = v['alternate_url']
        formatted_v['employer'] = v['employer']['name']
        formatted_v['requirement'] = v['snippet']['requirement']

        formatted_vacancies.append(formatted_v)

    return formatted_vacancies


def create_database(data_base_name: str, params):
    pass


def save_data_to_database(data: list, data_base_name: str, params):
    pass
