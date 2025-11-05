import random
class KATTLEBELL:

    def __init__(self, weight):
        self.weight = int(weight)
    def __repr__(self):
        return str(self.weight)
    def __eq__(self, other):
        return self.weight == other


class ITEM:
    def __init__(self):
        self.weight = random.randrange(1,100)

class SCALES:
    def __init__(self):
        self.kettlebells = []
        self.Item = ITEM()
        # print(self.Item.weight)

    def get_kettlebells(self):
        print(f"На правой чаще лежат гири: {self.kettlebells}")

    def leftweight(self):
        weight = sum([i.weight for i in self.kettlebells])
        return weight
    def check(self):
        if self.Item.weight > self.leftweight():
            print("Предмет весит больше гирь")
        elif self.Item.weight < self.leftweight():
            print("Предмет весит меньше гирь")
        else:
            print(f"Весы уравновешаны, вес предмета: {self.Item.weight}")
            return 0

        self.get_kettlebells()
    def checkTRUE(self):
        return self.Item.weight == self.leftweight()
    def add_kattlebell(self):
        try:
            weightKattlebell = int(input("Введите вес гири (1,2,5,10,...), которую хотите положить: "))
        except:
            print("Вес гири введен некорректно")
            return 0
        if weightKattlebell > 0 and (weightKattlebell in [1, 2] or weightKattlebell % 5 == 0):
            self.kettlebells.append(KATTLEBELL(weightKattlebell))
            self.check()
        else:
            print("ошибка")
            self.get_kettlebells()

    def del_kattlebell(self):
        del_weight = input("Введите вес гири, которую вы хотите убрать: ")
        try:
            self.kettlebells.remove(KATTLEBELL(del_weight))
            self.check()
        except:
            print("Ошибка")
            self.get_kettlebells()

A = SCALES()


while True:
    if A.checkTRUE():
        break
    interf = """1 - Положить гирю
2 - Удалить гирю
3 - Выход"""
    print(interf)
    req = input("Введите комманду: ")

    if req == str(1):
        A.add_kattlebell()
    elif req == str(2):
        A.del_kattlebell()
    elif req == str(3):
        break