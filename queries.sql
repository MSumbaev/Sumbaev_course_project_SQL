-- Удаление и создание базы данных
DROP DATABASE database_name;
CREATE DATABASE database_name;

-- Создание таблиц
CREATE TABLE employers (
    employer_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    url VARCHAR NOT NULL,
    site_url VARCHAR,
    city VARCHAR(50),
    description TEXT
);

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
);

-- Список всех компаний и количество вакансий у каждой компании.
SELECT employers.title, COUNT(*) FROM vacancies
INNER JOIN employers USING(employer_id)
GROUP BY employers.title;

-- Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
SELECT employers.title, vacancies.title, salary, vacancies.url
FROM vacancies
INNER JOIN employers USING(employer_id);

-- Список компаний и среднюю зарплату по всем вакансиям от этой компании.
SELECT employers.title, ROUND(AVG(salary)) FROM vacancies
INNER JOIN employers USING(employer_id)
WHERE salary IS NOT NULL
GROUP BY employers.title;

-- Список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT * FROM vacancies
WHERE salary > (SELECT AVG(salary) FROM vacancies);

-- Список всех вакансий, в названии которых содержатся искомые слова.
SELECT * FROM vacancies
WHERE lower(title) LIKE '%keyword.lower()%';
