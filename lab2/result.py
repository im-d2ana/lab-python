
n = 8
sum = 0
i = 0

while i < n:
    if i % 2 == 0  and  i != 4:
        print("Четное: ", i)
        j = 0
        while j < 2:
            if (j != 0)  or  i > 3:
                print("j = ", j)
            sum = sum + i + j
            j += 1
    elif (i % 3 != 0)  and  i != 1:
        print("Не кратно 3 и не 1: ", i)

    i += 1

message = "Сумма: "
isPositive = sum > 0

if isPositive  and  (sum >= 30):
    print(message, sum)
    if (sum % 2 == 0):
        print("Четная сумма")
    else:
        print("Нечетная сумма")
elif isPositive == False:
    print("Сумма не положительная")
else:
    print("Сумма малая")

counter = 0
while (counter < 2):
    print("Счетчик: ", counter)
    y = 0
    while y < 2:
        if (y == 0)  and  (counter == 1):
            print("Особая точка")
        y = y + 1
    counter = counter + 1

a = 5
b = 10

if (a < b)  and  (b > 8):
    print("a < b и b > 8")
    if (a == 5)  or  (b == 10):
        print("Значения стандартные")
