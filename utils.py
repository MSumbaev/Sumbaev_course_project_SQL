import psycopg2
import requests


def get_hh_data(employers_id: list):
    """Получение данных о работодателях и вакансиях с помощью API hh.ru"""
    data = []

    for employer_id in employers_id:

        response_emp = requests.get(f'https://api.hh.ru/employers/{employer_id}')

        employer_data = response_emp.json()

        vacancies_data = []
        count_page = (int(employer_data['open_vacancies']) // 100) + 1
        # Ограничение API на получение вакансий. Не больше 2000 вакансий
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
            'employer': employer_data,
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
            formatted_v['salary'] = None
            formatted_v['currency'] = None
        elif (v['salary']['from'] is not None) and (v['salary']['to'] is not None):
            formatted_v['salary'] = round((v['salary']['from'] + v['salary']['to']) / 2)
            formatted_v['currency'] = v['salary']['currency']
        elif v['salary']['from'] is not None:
            formatted_v['salary'] = v['salary']['to']
            formatted_v['currency'] = v['salary']['currency']
        elif v['salary']['to'] is not None:
            formatted_v['salary'] = v['salary']['from']
            formatted_v['currency'] = v['salary']['currency']

        formatted_v['city'] = None if v['address'] is None else v['address']['city']
        formatted_v['url'] = v['alternate_url']
        formatted_v['employer'] = v['employer']['name']
        formatted_v['published_at'] = v['published_at']
        formatted_v['requirement'] = v['snippet']['requirement']

        formatted_vacancies.append(formatted_v)

    return formatted_vacancies


def create_database(database_name: str, params):
    """Создание базы данных и таблиц для сохранения данных о работадателях и вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")
    except psycopg2.errors.InvalidCatalogName:
        cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    url VARCHAR NOT NULL,
                    site_url VARCHAR,
                    city VARCHAR(50),
                    description TEXT
                )
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    title VARCHAR NOT NULL,
                    salary INT,
                    currency VARCHAR(5),
                    city VARCHAR(50),
                    url VARCHAR NOT NULL,
                    publish_date DATE,
                    requirement TEXT
                )
            """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list, database_name: str, params):
    """Сохранение данных о работодателях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            employer_data = employer['employer']
            cur.execute(
                """
                INSERT INTO employers (title, url, site_url, city, description)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING employer_id
                """,
                (employer_data['name'], employer_data['alternate_url'], employer_data['site_url'],
                 employer_data['area']['name'], employer_data['description'])
            )

            employer_id = cur.fetchone()[0]
            vacancies_data = employer['vacancies']
            for vacancies in vacancies_data:
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, title, salary, currency,
                    city, url, publish_date, requirement)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (employer_id, vacancies['name'], vacancies['salary'], vacancies['currency'],
                     vacancies['city'], vacancies['url'], vacancies['published_at'], vacancies['requirement'])
                )

    conn.commit()
    conn.close()
