import psycopg2

from services.dbconnect import conn
from data.data_with_employer import list_with_employer
from services.input_error import Input_error


class DBManager():
    # добавить метод проверки по айди в бд
    """подключается к БД PostgreSQL. Имеет следующие функции:

    get_companies_and_vacancies_count() — получает список всех компаний
    и количество вакансий у каждой компании.

    get_all_vacancies()— получает список всех вакансий с указанием
    названия компании, названия вакансии и зарплаты и ссылки на вакансию.

    get_avg_salary() — получает среднюю зарплату по вакансиям.

    get_vacancies_with_higher_salary() — получает список всех вакансий,
    у которых зарплата выше средней по всем вакансиям.

    get_vacancies_with_keyword() — получает список всех вакансий,
    в названии которых содержатся переданные в метод слова, например python.
    """

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        # select distinct name_employer from vacancies
        # select count(name_employer) from vacancies where name_employer = 'Яндекс'
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT name_employer, COUNT(*) as count_vacancy FROM vacancies group by name_employer;")
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except psycopg2.InterfaceError:
            print('ошибка в получении вакансии')

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием
        названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT vacancies.name_employer, vacancies.name_vacancies, (vacancies.salary_min + vacancies.salary_max)/2 as salary, url "
                        f"FROM vacancies")
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except psycopg2.InterfaceError:
            print('ошибка в получении вакансии')

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT ROUND(AVG(vacancies.salary_min + vacancies.salary_max)/2) "
                        f"FROM vacancies;")
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except psycopg2.InterfaceError:
            print('ошибка в получении вакансии')

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT name_employer, name_vacancies, url "
                        f"FROM vacancies "
                        f"WHERE salary_min > (SELECT ROUND(AVG((salary_min + salary_max)/2)) "
                        f"FROM vacancies WHERE vacancies.salary_min<>0 and vacancies.salary_max<>0);")
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except psycopg2.InterfaceError:
            print('ошибка в получении вакансии')

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT name_employer, name_vacancies, requirement, url 
                        FROM vacancies 
                        WHERE requirement LIKE %s;
                        """,
                        (f"%{keyword}%",)
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except psycopg2.InterfaceError:
            print('ошибка в получении вакансии')
