from tools.dbloader import DBLoader
from tools.dbmanager import DBManager
import time
from data.data_with_employer import list_with_employer


def main_theme():
    begin = DBLoader()
    begin.big_red_button("vacancies")
    for employer in list_with_employer:
        begin.data_preparation_and_load_in_db(begin.get_vacancies(employer))
    print("Введите 1 если хотите воспользоваться уже сформированным списком работодателей\n"
          "Введите 2 если хотите добавить работодателя в список\n"
          "Введите 6 для выхода")
    step1 = input()
    if step1 == "1":
        print('загрузка данных...')
        time.sleep(0.4)
        print('.')
        time.sleep(0.4)
        print('..')
        time.sleep(0.4)
        print('...')
        time.sleep(0.4)
        print('....')
        time.sleep(0.7)
        print('загрузка завершена\n')
        branch1()
    elif step1 == "2":
        branch2()
    elif step1 == "6":
        exit("Всего доброго")


def branch1():
    s = DBManager()
    print("Введите 1 для получения списка всех компаний и количество вакансий у каждой компании\n"
          "Введите 2 для получения списка всех вакансий с указанием "
          "названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          "Введите 3 для получения средней зарплаты по вакансиям\n"
          "Введите 4 для получения списка всех вакансий, у которых зарплата выше "
          "средней по всем вакансиям\n"
          "Введите 5 для получения списка вакансий по ключевому слову\n"
          "Введите 6 для перехода в меню выше\n")
    branch1_2 = input()
    if branch1_2 == '1':
        s.get_companies_and_vacancies_count()
        print()
        branch1()
    elif branch1_2 == '2':
        s.get_all_vacancies()
        print()
        branch1()
    elif branch1_2 == '3':
        s.get_avg_salary()
        print()
        branch1()
    elif branch1_2 == '4':
        s.get_vacancies_with_higher_salary()
        print()
        branch1()
    elif branch1_2 == '5':
        user_keyword = input('Вводите слово\n')
        s.get_vacancies_with_keyword(user_keyword)
        print()
        branch1()
    elif branch1_2 == "6":
        print()
        main_theme()


def branch2():
    print('Текущий список работодателей в БД:')
    print(list_with_employer)
    branch2_1 = input('Введите 1 чтобы добавить работодателя в список\n'
                      'Введите 6 для перехода в меню выше\n')
    if branch2_1 == "1":
        user_employer = input('Введите наименование работодателя:\n')
        list_with_employer.append(user_employer)
        print()
        branch2()
    elif branch2_1 == "6":
        print()
        main_theme()
