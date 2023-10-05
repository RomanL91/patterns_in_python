# Тестовое задание:
# //Реализуйте итератор календаря. Каждый день представлен в виде строки вида "1 января". 
# При вызове функции next() итератор выдаст следующий день. 
# По окончании перебора всех элементов возникнет ошибка StopIteration//


from __future__ import annotations
from datetime import date, timedelta
from collections.abc import Iterable, Iterator
from typing import List, Any


class CalendarIterator(Iterator):

    _position: int = None


    def __init__(self, collection: CollectionCalendarDays) -> None:
        self._collection = collection
        self._position = 0


    def __next__(self):
        """
        Возращает следующий элемент в коллекции.

        Raises:
            StopIteration: при достижении конца коллекции.

        Returns:
            _type_: элемент коллекции [Any]
        """
        try:
            value = self._collection[self._position]
            self._position += 1 
        except IndexError:
            raise StopIteration()

        return value


class CollectionCalendarDays(Iterable):

    def __init__(self, collection: List[str] = []) -> None:
        self._collection = collection


    def __iter__(self) -> CalendarIterator:
        """
        Вернет обьект итератора.

        Returns:
            CalendarIterator: итератор календаря.
        """
        return CalendarIterator(self._collection)


    def add_item(self, item: str):
        """
        Позволяет добавить элемент в коллекцию.

        Args:
            item (str): элемент коллекции.
        """
        self._collection.append(item)


    def add_items(self, items: List[str]):
        """
        Позволяет расширить коллекцию несколькими элементами.

        Args:
            items (List[str]): элементы, которыми будет расширена коллекция.
        """
        self._collection.extend(items)


# ===================================================================
#   Такого же поведения можно добиться и через функцию генератор,
# которая так же хранит свое состояние и способна отдавать управление
# выполнения программы.

def calendar_generator_datetime(start_calendar: date, end_calendar: date) -> str:
    """
    Возрашает по одному дню от начальной точки до конечной.

    Args:
        start_calendar (date): начальная точка
        end_calendar (date): конечная точка

    Returns:
        str: день и месяц

    Yields:
        Iterator[str]: итератор коллекции
    """
    while start_calendar <= end_calendar:
        yield start_calendar.strftime('%d %B')
        start_calendar += timedelta(days=1)


def calendar_generator_collect(ccollection: List[Any]|tuple[Any]) -> Any:
    for el in ccollection:
        yield el


if __name__ == "__main__":
    # Создадим себе коллекции при помоши спискового включения (оно быстрее)
    # Одну наполним объектами datetime
    start_calendar = date(2023, 10, 1) # точка старта коллекции
    collection_calendar_days_datetime = [
        (start_calendar + timedelta(days=day)).strftime('%d %B') for day in range(10)
    ]
    print(f'Коллекция календарных дней объекта datetime: \n{collection_calendar_days_datetime}') # покажем, что вышло

    # Другую наполним объектами строк
    collection_calendar_days_string = [
        f'{i} января' for i in range(1, 9)
    ]
    print(f'Коллекция календарных дней: \n{collection_calendar_days_string}') # покажем, что вышло
    # print("\n")
    print("=" * 80, end="\n\n")

    # ===================================================================

    # Первый вариант, в котором StopIteration будет не "явным" и перебор
    # коллекции прекратится
    collection = CollectionCalendarDays() # создаем объект коллекции календаря
    collection.add_items(collection_calendar_days_datetime) # добавляем в него "заготовку"

    print("Запускаем перебор коллекции через наш итератор:")
    print("\n".join(collection))
    print("Это был пример обычной работы паттерна")
    print("=" * 80)
    
    print("Явно создаем обьект итератора и отдаем ему коллекцию [datetime]")
    calendar_iterator = CalendarIterator(collection=collection_calendar_days_datetime)
    print("Начинаем перебор итератора в цикле, тем самым делаем next()")
    for i in calendar_iterator:
        print(i)
    print("После истощения итератора вызываем еще раз функцию next()")
    print("Получаем исключение StopIteration: \n")
    # next(calendar_iterator)       # <<--- раскомментировать, чтобы получить исключение
    print("=" * 80)

    print("Явно создаем обьект итератора и отдаем ему коллекцию [string]")
    calendar_iterator = CalendarIterator(collection=collection_calendar_days_string)
    print("Начинаем перебор итератора в цикле, тем самым делаем next()")
    for i in calendar_iterator:
        print(i)
    print("После истощения итератора вызываем еще раз функцию next()")
    print("Получаем исключение StopIteration: \n")
    # next(calendar_iterator)       # <<--- раскомментировать, чтобы получить исключение
    print("=" * 80)

    print("На генераторе с datetime: \n")
    generator_calendar = calendar_generator_datetime(date(2023, 9, 1), date(2023, 9, 3))
    for i in generator_calendar:
        print(i)
    print("После истощения итератора вызываем еще раз функцию next()")
    print("Получаем исключение StopIteration: \n")
    # next(generator_calendar)      # <<--- раскомментировать, чтобы получить исключение
    print("=" * 80)

    print("На генераторе с любой коллекцией: \n")
    generator_calendar = calendar_generator_collect(collection_calendar_days_string)
    for i in generator_calendar:
        print(i)
    print("После истощения итератора вызываем еще раз функцию next()")
    print("Получаем исключение StopIteration: \n")
    # next(generator_calendar)      # <<--- раскомментировать, чтобы получить исключение
    print("=" * 80)
