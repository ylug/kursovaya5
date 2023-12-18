import requests

url = 'https://api.hh.ru/vacancies'
response = requests.get(url)
s = response.json()


def test_get_from_hhru():
    assert s != None
