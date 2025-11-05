import math
import matplotlib.pyplot as plt
import numpy as np

e= 0.001 # Погрешность

def F(x) -> float:
    t = 2
    return math.sqrt(1 - x**2) - (t**2)* (x**5)

def g(x):
    return F(x) + x

#Производные
def proizv(f, x, dx = 0.000001):
    return (f(x +dx) - f(x))/dx


#Отделение отрезка, на котором находится корень
def get_limits():
    otv = []
    for i in range(-30,30+1):
        try:
            if abs(F(i/10)) < 1e-10:
                otv.append((i/10,i/10))
            if abs(F((i+1)/10)) < 1e-10:
                otv.append(((i+1)/10,(i+1)/10))
            if (F(i/10) * F((i+1)/10) <0):
                otv.append((i/10, (i+1)/10))
        except(ValueError):
            continue

    pos = [i for i in otv if i[0] >0]
    if pos:
        return min(pos, key=lambda x: x[0])
    return max(otv, key=lambda x: x[0])


#Реализация метода простых итераций
def simple():
    a, b = get_limits()
    # a,b = [0.6, 0.8]
    x_0= (a+b)/2
    q = max([abs(proizv(g, i)) for i in np.arange(a, b, 0.01)])
    # q = max([abs(proizv(g, i)) for i in np.arange(a, b, 0.01)])
    if q >= 1:
        print(f"Метод не сходится q >= 1, q = {q:.4f}")
    max_iter = 100
    for i in range(max_iter):
        try:
            xk1 = g(x_0)
            print(f"Итерация {i}: x_{i} = {x_0:.5f}, x_{i + 1} = {xk1:.5f}")
            if abs(xk1 - x_0) <=((1-q)/q)*e:
                print(f"Корень найден: x = {xk1:.5f}")
                return xk1
            x_0 = xk1
        except:
            break
    print(f"Не сходится, x не принадлежит промежутку {[a,b]}")
    return None


def sec():
    x_0, x_1 = get_limits()
    x = [x_0, x_1]
    print(f"№  {'x0':<12} {'x1':<12} {'x2':<12} ")
    for k in range(1,1000):
        # Вычисляем значения функции
        F_xk = F(x[k])
        F_xk_1 = F(x[k - 1])

        # Формула метода секущих
        xk_1 = x[k] - (F_xk * (x[k] - x[k - 1])) / (F_xk - F_xk_1)
        x.append(xk_1)

        # Разность между текущим и предыдущим приближением
        delta = abs(xk_1 - x[k])

        # Вывод информации об итерации
        print(f"{k}: {x[k - 1]:<12.6f} {x[k]:<12.7f} {xk_1:<12.7f}")

        # Условие остановки
        if delta < e:
            print("-" * 70)
            print(f"Достигнута требуемая точность ε = {e}")
            break

    print(f"Корень найден: x = {x[-1]:.8f}")
    return x[-1]


print("Метод простых итераций")
print("="*50)
koren_simple = simple()
print()
print("Метод секущих")
print("="*50)
koren = sec()

#График с ответом
r = np.arange(-1,1, 0.01)
data = [F(x) for x in r]
fig, axes = plt.subplots()
axes.plot(r, data, label= "F(x)")
axes.scatter(koren,0, label = f"Искомая точка {koren:.3f}", color = "red")
axes.grid()
axes.legend()
plt.show()