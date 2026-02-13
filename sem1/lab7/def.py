
array = list(map(int, input('Введите список (числа через пробел): ').split()))

for i in range(len(array)):
    # Проверка числа на простоту
    for j in range(2, int(array[i]**0.5 + 1)):
        if array[i] % j == 0:
            is_prime = False
            break
    else:
        is_prime = True

    counter = 0
    while not(is_prime):# замена числа на ближайшее простое меньшее данного
        counter += 1

        # Проверка числа меньшего на counter на простоту
        for j in range(2, int((array[i] - counter) ** 0.5 + 1)):
            if (array[i] - counter) % j == 0:
                is_prime = False
                break
        else:
            is_prime = True

    array[i] = array[i] - counter

print('Измененный список: ', *array)