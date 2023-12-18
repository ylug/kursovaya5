# добавляет данные в БД
import psycopg2
from services.get_from_hhru import HeadHunterAPI
from services.input_error import Input_error
from services.dbconnect import conn

from password import password


class DBLoader(HeadHunterAPI, Input_error):
    """обработка, загрузка данных в БД"""

    def __init__(self, vacancy_id=None, vacancy_name=None, vacancy_url=None,
                 vacancy_salary=None, vacancy_city=None, vacancy_requirement=None,
                 vacancy_responsibility=None, employer_name=None, employer_id=None):
        try:
            self.vacancy_id = vacancy_id
            self.vacancy_name = vacancy_name
            self.vacancy_url = vacancy_url
            self.vacancy_salary = vacancy_salary
            self.vacancy_city = vacancy_city
            self.vacancy_requirement = vacancy_requirement
            self.vacancy_responsibility = vacancy_responsibility
            self.employer_name = employer_name
            self.employer_id = employer_id
        except Input_error as s:
            print(s.message)

    def data_preparation_and_load_in_db(self, downloades_data):
        # Подключение к db
        try:
            with conn:
                with conn.cursor() as cur:
                    for item in downloades_data['items']:
                        salary = item['salary']
                        if salary is not None:
                            salary_min = salary['from']
                            salary_max = salary['to']
                            salary_currency = salary['currency'] if salary['currency'] else "Не указано"
                        else:
                            salary_min = 0
                            salary_max = 0
                            salary_currency = 'НЕТ'
                        vacancy = []
                        res = {
                            "id вакансии": int(item['id']),
                            "название работодателя": item["employer"]["name"],
                            "Название вакансии": item['name'],
                            "Заработная плата min": salary_min,
                            "Заработная плата max": salary_max,
                            "Валюта": salary_currency,
                            "Город": item["area"]["name"],
                            "Требование": item['snippet']['requirement'],
                            "Обязанности": item['snippet']['responsibility'],
                            "cсылка": item['url'],
                            "id работодателя": int(item["employer"]["id"]),
                        }
                        vacancy.append(res)
                        # print(vacancy)
                        # заполнение таблицы vacancies
                        cur.execute(
                            "INSERT INTO vacancies (id_vacancies, name_employer, name_vacancies,"
                            "salary_min, salary_max, salary_currency, city, requirement, responsibility, "
                            "url, id_employer)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                            (vacancy[0]["id вакансии"],
                             vacancy[0]["название работодателя"],
                             vacancy[0]["Название вакансии"],
                             vacancy[0]["Заработная плата min"],
                             vacancy[0]["Заработная плата max"],
                             vacancy[0]["Валюта"],
                             vacancy[0]["Город"],
                             vacancy[0]["Требование"],
                             vacancy[0]["Обязанности"],
                             vacancy[0]["cсылка"],
                             vacancy[0]["id работодателя"],
                             )
                        )

                    # rows = cur.fetchall()
                    # for row in rows:
                    #     print(row)
        except psycopg2.InterfaceError:
            print('не записано в бд')
        except psycopg2.errors.UniqueViolation:
            print('ошибка: повтор id вакансии')
        except TypeError:
            print()

    # # закрытие соединения
    #     finally:
    #         conn.close()

    def big_red_button(self, table_name):
        """Удаляет все данные из указанной таблицы"""
        # Подключение к db
        conn = psycopg2.connect(
            host="localhost",
            database="db_hh_ru",
            user="postgres",
            password=password
        )
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(f"DELETE FROM {table_name}")

        finally:
            # закрытие соединения
            conn.close()
