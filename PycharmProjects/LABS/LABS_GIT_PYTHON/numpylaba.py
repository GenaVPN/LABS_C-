import numpy


def n1():
    A = numpy.random.randint(0,100,100)
    print("Изначальная A:\n",A)
    A = A.reshape([10,10])
    print("Измененная A:\n",A)

def n2():
    A = numpy.random.randint(0,101,(5,5))
    B = numpy.random.randint(0,101,(5,5))
    print("Изначальная A:\n",A)
    print("Изначальная B:\n",B)
    print("A+B\n",A+B)
    print("A-B\n",A-B)
    print("A**2\n",A**2)
    print("A+100\n",A+100)
def n3():
    A = numpy.random.randint(0,100,(10,10))
    print("Изначальная: ")
    print(A)
    print("Транспонированная: ")
    print(A.transpose())
    print("Сортированная по строчкам")

    B = numpy.sort(A, 1)
    print(B)
    print("Сортированная по столбикам")
    B = numpy.sort(A, 0)
    print(B)


n1()
print("---"*100)
n2()
print("---"*100)
n3()