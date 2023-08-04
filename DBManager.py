import psycopg2
from config import config


class DBManager:

    def __init__(self, database_name='hh_ru', params=config()):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """Возвращает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.title, COUNT(*) FROM vacancies
                INNER JOIN employers USING(employer_id)
                GROUP BY employers.title 
                """
            )

            rows = cur.fetchall()

        conn.close()
        return rows

    def get_all_vacancies(self):
        """Возвращает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.title, vacancies.title, salary, vacancies.url
                FROM vacancies
                INNER JOIN employers USING(employer_id)
                """
            )

            rows = cur.fetchall()

        conn.close()
        return rows

    def get_avg_salary(self):
        """Возвращает список компаний и среднюю зарплату по всем вакансиям от этой компании."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.title, ROUND(AVG(salary)) FROM vacancies
                INNER JOIN employers USING(employer_id)
                WHERE salary IS NOT NULL
                GROUP BY employers.title
                """
            )

            rows = cur.fetchall()

        conn.close()
        return rows

    def get_vacancies_with_higher_salary(self):
        """Возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                """
            )

            rows = cur.fetchall()

        conn.close()
        return rows

    def get_vacancies_with_keyword(self, keyword: str):
        """Возвращает список всех вакансий, в названии которых содержатся переданные в метод слова,
         например “python”."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT * FROM vacancies
                WHERE lower(title) LIKE '%{keyword.lower()}%'
                """
            )

            rows = cur.fetchall()

        conn.close()
        return rows
