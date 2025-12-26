import heapq


def func(operation, *numbers, factor=1, degree=1):
    def find_min_max(method, operation, numbers):  # поиск мин. и макс. разными способами

        def built_in_min_max(operation, numbers):
            return min(numbers) if operation == 'min' else max(numbers)

        def passing_min_max(operation, numbers):
            n = numbers[0]
            for i in numbers:
                if operation == 'min' and i < n:
                    n = i
                elif operation == 'max' and i > n:
                    n = i
            return n

        def sort_min_max(operation, numbers):
            if operation == 'min':
                return sorted(numbers)[0]
            else:
                return sorted(numbers)[-1]

        def heap_min_max(operation, numbers):
            if operation == 'min':
                heap = list(numbers)
                heapq.heapify(heap)
                n = heap[0]
            else:
                heap = [-i for i in numbers]
                heapq.heapify(heap)
                n = -heap[0]
            return n

        match method:
            case '1':
                n = built_in_min_max(operation, numbers)
            case '2':
                n = passing_min_max(operation, numbers)
            case '3':
                n = sort_min_max(operation, numbers)
            case '4':
                n = heap_min_max(operation, numbers)
            case _:
                n = False

        return n

    if not numbers:
        return False

    match operation.strip():
        case 'min' | 'max':
            method = input('Введите способ нахождения минимума или максимума:\n'
                           '1) Встроенными функциями min или max\n'
                           '2) Прохождением по списку\n'
                           '3) Встроенной сортировкой\n'
                           '4) Кучами\n'
                           'Введите число: ')
            n = find_min_max(method, operation, numbers)
        case 'sum':
            n = sum(numbers)
        case 'average':
            n = sum(numbers) / len(numbers) if numbers else 0
        case _:
            return False

    return n * factor ** degree


print(func('max', 1, 2, 3, 4, 5, 5, 6, 7, 100, 8, 9, 9, 0, factor=2, degree=1))
