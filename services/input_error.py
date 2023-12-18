class Input_error(Exception):
    """Вывод ошибок в консоль"""

    def __init__(self):
        self.message = "Ошибка ввода данных"
