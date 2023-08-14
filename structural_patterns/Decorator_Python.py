# Декоратор - структурный паттерн проектирования, который позволяет динамически
# добовлять обьектам новую функциональность, оборачивая их в полезные "обертки".


class Component():
    """
    Базовый интерфейс Компонента определяет поведение, которое изменяется
    декораторами.
    """

    def operation(self) -> str:
        pass


class ConcreteComponent(Component):
    """
    Конкретные Компоненты предоставляют реализации поведения по умолчанию. Может
    быть несколько вариаций этих классов.
    """

    def operation(self) -> str:
        return "ConcreteComponent"
    

class Decorator(Component):
    """
    Базовый класс Декоратора следует тому же интерфейсу, что и другие
    компоненты. Основная цель этого класса - определить интерфейс обёртки для
    всех конкретных декораторов. Реализация кода обёртки по умолчанию может
    включать в себя поле для хранения завёрнутого компонента и средства его
    инициализации.
    """

    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        """
        Декоратор делегирует всю работу обёрнутому компоненту.
        """

        return self._component

    def operation(self) -> str:
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    """
    Конкретные Декораторы вызывают обёрнутый объект и изменяют его результат
    некоторым образом.
    """

    def operation(self) -> str:
        """
        Декораторы могут вызывать родительскую реализацию операции, вместо того,
        чтобы вызвать обёрнутый объект напрямую. Такой подход упрощает
        расширение классов декораторов.
        """
        return f"ConcreteDecoratorA({self.component.operation()})"


class ConcreteDecoratorB(Decorator):
    """
    Декораторы могут выполнять своё поведение до или после вызова обёрнутого
    объекта.
    """

    def operation(self) -> str:
        return f"ConcreteDecoratorB({self.component.operation()})"


def client_code(component: Component) -> None:
    """
    Клиентский код работает со всеми объектами, используя интерфейс Компонента.
    Таким образом, он остаётся независимым от конкретных классов компонентов, с
    которыми работает.
    """

    # ...

    print(f"RESULT: {component.operation()}", end="")

    # ...


# if __name__ == "__main__":
#     # Таким образом, клиентский код может поддерживать как простые компоненты...
#     simple = ConcreteComponent()
#     print("Client: I've got a simple component:")
#     client_code(simple)
#     print("\n")

#     # ...так и декорированные.
#     #
#     # Обратите внимание, что декораторы могут обёртывать не только простые
#     # компоненты, но и другие декораторы.
#     decorator1 = ConcreteDecoratorA(simple)
#     decorator2 = ConcreteDecoratorB(decorator1)
#     print("Client: Now I've got a decorated component:")
#     client_code(decorator2)

    
    

# ================================================================================
    # еще примеры...


def my_shiny_new_decorator(function_to_decorate):
    # Внутри себя декоратор определяет функцию-"обёртку". Она будет обёрнута вокруг декорируемой,
    # получая возможность исполнять произвольный код до и после неё.
    def the_wrapper_around_the_original_function():
        print("Я - код, который отработает до вызова функции")
        function_to_decorate() # Сама функция
        print("А я - код, срабатывающий после")
    # Вернём эту функцию
    return the_wrapper_around_the_original_function


# Представим теперь, что у нас есть функция, которую мы не планируем больше трогать.
# обернули в декоратор
@my_shiny_new_decorator
def stand_alone_function():
    print("Я простая одинокая функция, ты ведь не посмеешь меня изменять?")


# if __name__ == "__main__":
#     stand_alone_function()
# декорировать функции можно несколькоми декораторами, при этом нужно помнить о порядке!



# Передача декоратором аргументов в функцию
def a_decorator_passing_arguments(function_to_decorate):
    def a_wrapper_accepting_arguments(arg1, arg2):
        print("Смотри, что я получил:", arg1, arg2)
        function_to_decorate(arg1, arg2)
    return a_wrapper_accepting_arguments


# Теперь, когда мы вызываем функцию, которую возвращает декоратор, мы вызываем её "обёртку",
# передаём ей аргументы и уже в свою очередь она передаёт их декорируемой функции
@a_decorator_passing_arguments
def print_full_name(first_name, last_name):
    print("Меня зовут", first_name, last_name)


# if __name__ == "__main__":
    # print_full_name('Roman', 'Lebedev')
    


# Пример декоратора для приминения к функции\методу с использованием распаковки аргументов
def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    # Данная "обёртка" принимает любые аргументы
    def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        print("Передали ли мне что-нибудь?:")
        print(args)
        print(kwargs)
        function_to_decorate(*args, **kwargs)
    return a_wrapper_accepting_arbitrary_arguments


@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    print("Python is cool, no argument here.")


@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print(a, b, c)


@a_decorator_passing_arbitrary_arguments
def function_with_named_arguments(a, b, c, platypus="Почему нет?"):
    print("Любят ли {}, {} и {} утконосов? {}".format(a, b, c, platypus))


class Mary(object):
    def __init__(self):
        self.age = 31
    @a_decorator_passing_arbitrary_arguments
    def sayYourAge(self, lie=-3): # Теперь мы можем указать значение по умолчанию
        print("Мне {} лет, а ты бы сколько дал?".format(self.age + lie))


if __name__ == "__main__":
    function_with_no_argument()
    print('='*33)
    function_with_arguments(1, 2, 3)
    print('='*33)
    function_with_named_arguments("Билл", "Линус", "Стив", platypus="Определенно!")
    print('='*33)

    m = Mary()
    m.sayYourAge()
    print('='*33)
    m.sayYourAge(lie=0) # если честный ответ


# Некоторые особенности работы с декораторами
# Декораторы несколько замедляют вызов функции, не забывайте об этом.
# Вы не можете "раздекорировать" функцию. Безусловно, существуют трюки, позволяющие создать декоратор, 
# который можно отсоединить от функции, но это плохая практика. 
# Правильнее будет запомнить, что если функция декорирована — это не отменить.
# Декораторы оборачивают функции, что может затруднить отладку.
