from math import tan
import matplotlib.pyplot as plt

# Определение функции f(x)
def f(x):
    return tan(x) ** 2 - x


# Определение функции g(x), где g(x) = x + f(x)
def g(x):
    return tan(x) ** 2


# Функция для подсчёта производной f(x)
def derivative_f(x, dx=0.0000001):
    return (f(x + dx) - f(x)) / dx



# Аналогичная функция для подсчёта производной g(x)
def derivative_g(x, dx=0.0000001):
    return (g(x + dx) - g(x)) / dx


# Функция для отделения корня уравнения
def get_limits():
    left_list = list()
    right_list = list()
    for x in range(10):
        current_f = f(x / 10)
        if current_f > 0:
            right_list.append(x / 10)
        else:
            left_list.append(x / 10)

    if right_list:
        b = min(right_list)
    else:
        b = None

    if left_list:
        a = max(left_list)
    else:
        a = None
    return a, b




# Реализация метода простой итерации
def simple_iteration():
    print("--------------------Метод простой итерации-----------	---------")
    a, b = get_limits()
    xk = (a + b) / 2

    # Проверка сходимости метода
    if derivative_g(xk) > 1:
        print(f"Производная g'(x) = {derivative_g(xk):.3f}, g'(x) 		> 1")
        print("Метод простой итерации не будет сходиться для 			заданной функции.")
        return None

    while a < xk < b:
        xk1 = g(xk)
        print(f"xk = {xk:.5f}, xk1 = {xk1:.5f}")
        if abs(xk1 - xk) <= 0.001:
            return xk1
        xk = xk1
    print("Метод простой итерации не сходится.")
    return None



# Реализация метода касательных (Ньютона)
def newton_method():
    print("-----------------Метод касательных (Ньютона)---------	---------")
    a, b = get_limits()
    xk = (a + b) / 2
    xk_values = [xk]
    for i in range(10):
        xk1 = xk - f(xk) / derivative_f(xk)

        if abs(xk1 - xk) <= 0.001:
            print("Условие сходимости выполняется на", i + 1, 				"итерации.")
            break

        xk = xk1
        xk_values.append(xk)

    return xk


# Функция для построения графика с выделением корня
def plot_function(root):
    x_values = [x / 10.0 for x in range(-50, 51)]
    y_values = [f(x) for x in x_values]

    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, label='f(x) = tan(x)^2 - x', 	color='blue')
    plt.axhline(0, color='black', linewidth=1, ls='-')
    plt.axvline(0, color='black', linewidth=1, ls='-')

    # Выделение корня
    plt.plot(root, f(root), 'ro', label=f'Корень: x = 	{root:.3f}')

    plt.title('График функции f(x)')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.ylim(-7, 7)  # Ограничение по оси y для лучшей видимости
    plt.grid()
    plt.legend()
    plt.savefig("graph_function.png")
    plt.show()


# Запуск методов
result_simple_iteration = simple_iteration()
print("Результат метода простой итерации:", result_simple_iteration)

result_newton_method = newton_method()
print(f"Результат метода Ньютона: {result_newton_method:.3f}")

# Построение графика функции с выделением корня
plot_function(result_newton_method)
