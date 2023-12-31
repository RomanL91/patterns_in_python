# Абстрактная фабрика — это порождающий паттерн проектирования, 
# который позволяет создавать семейства связанных объектов, 
# не привязываясь к конкретным классам создаваемых объектов.

# ====================== Описание проблемы:
# Представьте, что вы пишете симулятор мебельного магазина. 
# Ваш код содержит:
# Семейство зависимых продуктов. Скажем, Кресло + Диван + Столик.
# Несколько вариаций этого семейства. 
# Например, продукты Кресло, Диван и Столик представлены 
# в трёх разных стилях: Ар-деко, Викторианском и Модерне.

# Вам нужен такой способ создавать объекты продуктов, чтобы они сочетались 
# с другими продуктами того же семейства. Это важно, так как клиенты расстраиваются, 
# если получают несочетающуюся мебель.

# Кроме того, вы не хотите вносить изменения в существующий код при 
# добавлении новых продуктов или семейcтв в программу. Поставщики часто обновляют 
# свои каталоги, и вы бы не хотели менять уже написанный код каждый 
# раз при получении новых моделей мебели.

# ====================== РЕШЕНИЕ:
# Для начала паттерн Абстрактная фабрика предлагает выделить общие интерфейсы для 
# отдельных продуктов, составляющих семейства. Так, все вариации кресел получат 
# общий интерфейс Кресло, все диваны реализуют интерфейс Диван и так далее.
# Далее вы создаёте абстрактную фабрику — общий интерфейс, который содержит методы 
# создания всех продуктов семейства (например, создатьКресло, создатьДиван и создатьСтолик). 
# Эти операции должны возвращать абстрактные типы продуктов, представленные интерфейсами, 
# которые мы выделили ранее — Кресла, Диваны и Столики.

# Как насчёт вариаций продуктов? Для каждой вариации семейства продуктов мы должны 
# создать свою собственную фабрику, реализовав абстрактный интерфейс. 
# Фабрики создают продукты одной вариации. Например, ФабрикаМодерн будет возвращать 
# только КреслаМодерн,ДиваныМодерн и СтоликиМодерн.

# Клиентский код должен работать как с фабриками, так и с продуктами только через 
# их общие интерфейсы. Это позволит подавать в ваши классы любой тип фабрики и 
# производить любые продукты, ничего не ломая.

# Например, клиентский код просит фабрику сделать стул. Он не знает, какого типа была эта фабрика. 
# Он не знает, получит викторианский или модерновый стул. Для него важно, 
# чтобы на стуле можно было сидеть и чтобы этот стул отлично смотрелся с диваном той же фабрики.

# Осталось прояснить последний момент: кто создаёт объекты конкретных фабрик, 
# если клиентский код работает только с интерфейсами фабрик? 
# Обычно программа создаёт конкретный объект фабрики при запуске, причём тип фабрики выбирается, 
# исходя из параметров окружения или конфигурации.


from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    """
    Интерфейс Абстрактной Фабрики объявляет набор методов, которые возвращают
    различные абстрактные продукты. Эти продукты называются семейством и связаны
    темой или концепцией высокого уровня. Продукты одного семейства обычно могут
    взаимодействовать между собой. Семейство продуктов может иметь несколько
    вариаций, но продукты одной вариации несовместимы с продуктами другой.
    """
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass


class ConcreteFactory1(AbstractFactory):
    """
    Конкретная Фабрика производит семейство продуктов одной вариации. Фабрика
    гарантирует совместимость полученных продуктов. Обратите внимание, что
    сигнатуры методов Конкретной Фабрики возвращают абстрактный продукт, в то
    время как внутри метода создается экземпляр конкретного продукта.
    """

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()


class ConcreteFactory2(AbstractFactory):
    """
    Каждая Конкретная Фабрика имеет соответствующую вариацию продукта.
    """

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()


class AbstractProductA(ABC):
    """
    Каждый отдельный продукт семейства продуктов должен иметь базовый интерфейс.
    Все вариации продукта должны реализовывать этот интерфейс.
    """

    @abstractmethod
    def useful_function_a(self) -> str:
        pass


"""
Конкретные продукты создаются соответствующими Конкретными Фабриками.
"""


class ConcreteProductA1(AbstractProductA):
    def useful_function_a(self) -> str:
        return "The result of the product A1."


class ConcreteProductA2(AbstractProductA):
    def useful_function_a(self) -> str:
        return "The result of the product A2."


class AbstractProductB(ABC):
    """
    Базовый интерфейс другого продукта. Все продукты могут взаимодействовать
    друг с другом, но правильное взаимодействие возможно только между продуктами
    одной и той же конкретной вариации.
    """
    @abstractmethod
    def useful_function_b(self) -> None:
        """
        Продукт B способен работать самостоятельно...
        """
        pass

    @abstractmethod
    def another_useful_function_b(self, collaborator: AbstractProductA) -> None:
        """
        ...а также взаимодействовать с Продуктами A той же вариации.

        Абстрактная Фабрика гарантирует, что все продукты, которые она создает,
        имеют одинаковую вариацию и, следовательно, совместимы.
        """
        pass


"""
Конкретные Продукты создаются соответствующими Конкретными Фабриками.
"""


class ConcreteProductB1(AbstractProductB):
    def useful_function_b(self) -> str:
        return "The result of the product B1."

    """
    Продукт B1 может корректно работать только с Продуктом A1. Тем не менее, он
    принимает любой экземпляр Абстрактного Продукта А в качестве аргумента.
    """

    def another_useful_function_b(self, collaborator: AbstractProductA) -> str:
        result = collaborator.useful_function_a()
        return f"The result of the B1 collaborating with the ({result})"


class ConcreteProductB2(AbstractProductB):
    def useful_function_b(self) -> str:
        return "The result of the product B2."

    def another_useful_function_b(self, collaborator: AbstractProductA):
        """
        Продукт B2 может корректно работать только с Продуктом A2. Тем не менее,
        он принимает любой экземпляр Абстрактного Продукта А в качестве
        аргумента.
        """
        result = collaborator.useful_function_a()
        return f"The result of the B2 collaborating with the ({result})"


def client_code(factory: AbstractFactory) -> None:
    """
    Клиентский код работает с фабриками и продуктами только через абстрактные
    типы: Абстрактная Фабрика и Абстрактный Продукт. Это позволяет передавать
    любой подкласс фабрики или продукта клиентскому коду, не нарушая его.
    """
    product_a = factory.create_product_a()
    product_b = factory.create_product_b()

    print(f"{product_b.useful_function_b()}")
    print(f"{product_b.another_useful_function_b(product_a)}", end="")


if __name__ == "__main__":
    """
    Клиентский код может работать с любым конкретным классом фабрики.
    """
    print("Client: Testing client code with the first factory type:")
    client_code(ConcreteFactory1())

    print("\n")

    print("Client: Testing the same client code with the second factory type:")
    client_code(ConcreteFactory2())