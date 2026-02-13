
def bubble(arr):
    arr = arr.copy()
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def flag_bubble(arr):
    arr = arr.copy()
    for i in range(len(arr) - 1):
        is_swapped = False
        for j in range(len(arr) - i - 1):
            if arr[j + 1] < arr[j]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                is_swapped = True

        if not is_swapped:
            break

    return arr


def insertion(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


def binary_insertion(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        low, high = 0, i

        while low < high:
            mid = low + (low + high) // 2
            if key < arr[mid]:
                high = mid
            else:
                low = mid + 1

        for j in range(i, low, -1):
            arr[j] = arr[j - 1]

        arr[low] = key

    return arr


def barrier_insertion(arr):
    arr = [0] + arr
    for i in range(1, len(arr)):
        arr[0] = arr[i]
        j = i - 1
        while arr[0] < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = arr[0]
    return arr[1:]


def selection(arr):
    arr = arr.copy()
    for i in range(len(arr) - 1):
        mn = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[mn]:
                mn = j

        arr[mn], arr[i] = arr[i], arr[mn]

    return arr


def shell(arr):
    arr = arr.copy()
    inc = len(arr) // 2
    while inc > 0:
        for i in range(len(arr)):
            key = arr[i]
            while i >= inc and key < arr[i - inc]:
                arr[i] = arr[i - inc]
                i -= inc
            arr[i] = key
        inc //= 2

    return arr


def shaker(arr):
    arr = arr.copy()
    left = 0
    right = len(arr) - 1
    while left <= right:
        for i in range(left, right, 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]

        right -= 1

        for i in range(right, left, -1):
            if arr[i - 1] > arr[i]:
                arr[i - 1], arr[i] = arr[i], arr[i - 1]

        left += 1

    return arr



# Quick sort

def recursive_quick_sort(arr):

    if len(arr) < 2:
        return arr

    pivot = arr[len(arr) // 2]
    low, mid, high = [],[],[]
    for i in arr:
        if i < pivot:
            low.append(i)
        elif i > pivot:
            high.append(i)
        else:
            mid.append(i)

    return recursive_quick_sort(low) + mid + recursive_quick_sort(high)



def part(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = part(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

    return arr


lst = list(range(100, -1, -1))
sorted_lst = sorted(lst)

print(bubble(lst))  # True
print(flag_bubble(lst))  # True
print(insertion(lst))  # True
print(binary_insertion(lst))  # True
print(barrier_insertion(lst))  # True
print(selection(lst))  # True
print(shell(lst))  # True
print(shaker(lst))  # True

# Quick sort
print(recursive_quick_sort(lst)) # True
print(quick_sort(lst, 0, len(lst) - 1)) # True

print(lst)
