# Итератор — это поведенческий паттерн проектирования, который даёт возможность последовательно 
# обходить элементы составных объектов, не раскрывая их внутреннего представления.

# Проблема
# Коллекции — самая распространённая структура данных, которую вы можете встретить в программировании. 
# Это набор объектов, собранный в одну кучу по каким-то критериям.

# Большинство коллекций выглядят как обычный список элементов. 
# Но есть и экзотические коллекции, построенные на основе деревьев, графов и других сложных структур данных.

# Но как бы ни была структурирована коллекция, пользователь должен иметь 
# возможность последовательно обходить её элементы, чтобы проделывать с ними какие-то действия.

# Но каким способом следует перемещаться по сложной структуре данных? 
# Например, сегодня может быть достаточным обход дерева в глубину, но завтра потребуется возможность перемещаться по дереву в ширину. 
# А на следующей неделе и того хуже — понадобится обход коллекции в случайном порядке

# Добавляя всё новые алгоритмы в код коллекции, вы понемногу размываете её основную задачу, 
# которая заключается в эффективном хранении данных. Некоторые алгоритмы могут быть и вовсе слишком «заточены» 
# под определённое приложение и смотреться дико в общем классе коллекции.


# Решение
# Идея паттерна Итератор состоит в том, чтобы вынести поведение обхода коллекции из самой коллекции в отдельный класс.

# Объект-итератор будет отслеживать состояние обхода, текущую позицию в коллекции и сколько элементов ещё осталось обойти. 
# Одну и ту же коллекцию смогут одновременно обходить различные итераторы, а сама коллекция не будет даже знать об этом.

# К тому же, если вам понадобится добавить новый способ обхода, 
# вы сможете создать отдельный класс итератора, не изменяя существующий код коллекции.


from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import Any, List


"""
Для создания итератора в Python есть два абстрактных класса из встроенного
модуля collections - Iterable, Iterator. Нужно реализовать метод __iter__() в
итерируемом объекте (списке), а метод __next__() в итераторе.
"""


class AlphabeticalOrderIterator(Iterator):
    """
    Конкретные Итераторы реализуют различные алгоритмы обхода. Эти классы
    постоянно хранят текущее положение обхода.
    """

    """
    Атрибут _position хранит текущее положение обхода. У итератора может быть
    множество других полей для хранения состояния итерации, особенно когда он
    должен работать с определённым типом коллекции.
    """
    _position: int = None

    """
    Этот атрибут указывает направление обхода.
    """
    _reverse: bool = False

    def __init__(self, collection: WordsCollection, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        """
        Метод __next __() должен вернуть следующий элемент в последовательности.
        При достижении конца коллекции и в последующих вызовах должно вызываться
        исключение StopIteration.
        """
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class WordsCollection(Iterable):
    """
    Конкретные Коллекции предоставляют один или несколько методов для получения
    новых экземпляров итератора, совместимых с классом коллекции.
    """

    def __init__(self, collection: List[Any] = []) -> None:
        self._collection = collection

    def __iter__(self) -> AlphabeticalOrderIterator:
        """
        Метод __iter__() возвращает объект итератора, по умолчанию мы возвращаем
        итератор с сортировкой по возрастанию.
        """
        return AlphabeticalOrderIterator(self._collection)

    def get_reverse_iterator(self) -> AlphabeticalOrderIterator:
        return AlphabeticalOrderIterator(self._collection, True)

    def add_item(self, item: Any):
        self._collection.append(item)


if __name__ == "__main__":
    # Клиентский код может знать или не знать о Конкретном Итераторе или классах
    # Коллекций, в зависимости от уровня косвенности, который вы хотите
    # сохранить в своей программе.
    collection = WordsCollection()
    collection.add_item("First")
    collection.add_item("Second")
    collection.add_item("Third")

    print("Straight traversal:")
    print("\n".join(collection))
    print("")

    print("Reverse traversal:")
    print("\n".join(collection.get_reverse_iterator()), end="")
    