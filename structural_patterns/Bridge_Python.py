# Мост - это структурный паттерн, который раздляет один или несколько
# классов на две отдельные иеархии - абстракцию и реализацию, 
# позволяя изменять их не зависимо друг от друга.

# Описание проблемы:
# У вас есть класс геометрических Фигур, который имеет подклассы Круг и Квадрат. 
# Вы хотите расширить иерархию фигур по цвету, то есть иметь Красные и Синие фигуры. 
# Но чтобы всё это объединить, вам придётся создать 4 комбинации подклассов, 
# вроде СиниеКруги и КрасныеКвадраты.
# При добавлении новых видов фигур и цветов количество комбинаций будет расти в геометрической прогрессии. 
# Например, чтобы ввести в программу фигуры треугольников, придётся создать сразу два новых подкласса 
# треугольников под каждый цвет. После этого новый цвет потребует создания уже трёх классов для всех видов фигур. 
# Чем дальше, тем хуже.
# 
# Решение:
# Паттерн Мост предлагает заменить наследование агрегацией или композицией. 
# Для этого нужно выделить одну из таких «плоскостей» в отдельную иерархию и 
# ссылаться на объект этой иерархии, вместо хранения его состояния и поведения 
# внутри одного класса.
# Таким образом, мы можем сделать Цвет отдельным классом с подклассами Красный и Синий. 
# Класс Фигур получит ссылку на объект Цвета и сможет делегировать ему работу, если потребуется. 
# Такая связь и станет мостом между Фигурами и Цветом. 
# При добавлении новых классов цветов не потребуется трогать классы фигур и наоборот.


from __future__ import annotations
from abc import ABC, abstractmethod


class Abstraction:
    """
    Абстракция устанавливает интерфейс для «управляющей» части двух иерархий
    классов. Она содержит ссылку на объект из иерархии Реализации и делегирует
    ему всю настоящую работу.
    """

    def __init__(self, implementation) -> None:
        self.implementation = implementation


    def operation(self) -> str:
        return (
            f'Abstraction: Base operation with:\n'
            f'{self.implementation.operation_implementation()}'
        )
    

class ExtendedAbstraction(Abstraction):
    """
    Можно расширить Абстракцию без изменения классов Реализации.
    """

    def operation(self) -> str:
        return (
            f"ExtendedAbstraction: Extended operation with:\n"
            f"{self.implementation.operation_implementation()}"
        )
    

class Implementation(ABC):
    """
    Реализация устанавливает интерфейс для всех классов реализации. Он не должен
    соответствовать интерфейсу Абстракции. На практике оба интерфейса могут быть
    совершенно разными. Как правило, интерфейс Реализации предоставляет только
    примитивные операции, в то время как Абстракция определяет операции более
    высокого уровня, основанные на этих примитивах.
    """

    @abstractmethod
    def operation_implementation(self) -> str:
        pass


# Каждая Конкретная Реализация соответствует определённой платформе и реализует
# интерфейс Реализации с использованием API этой платформы.


class ConcreteImplementationA(Implementation):
    def operation_implementation(self) -> str:
        return "ConcreteImplementationA: Here's the result on the platform A."


class ConcreteImplementationB(Implementation):
    def operation_implementation(self) -> str:
        return "ConcreteImplementationB: Here's the result on the platform B."


def client_code(abstraction: Abstraction) -> None:
    """
    За исключением этапа инициализации, когда объект Абстракции связывается с
    определённым объектом Реализации, клиентский код должен зависеть только от
    класса Абстракции. Таким образом, клиентский код может поддерживать любую
    комбинацию абстракции и реализации.
    """
    print(abstraction.operation(), end="")


if __name__ == "__main__":
    """
    Клиентский код должен работать с любой предварительно сконфигурированной
    комбинацией абстракции и реализации.
    """

    implementation = ConcreteImplementationA()
    abstraction = Abstraction(implementation)
    client_code(abstraction)

    print("\n")

    implementation = ConcreteImplementationB()
    abstraction = ExtendedAbstraction(implementation)
    client_code(abstraction)
