# 代码生成时间: 2025-09-17 10:04:06
import celery
def bubble_sort(numbers):
    # Bubble Sort algorithm implementation
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                # Swap if the element found is greater than the next element
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers
def quick_sort(numbers):
    # Quick Sort algorithm implementation
    if len(numbers) <= 1:
        return numbers
    else:
        pivot = numbers[0]
        less = [x for x in numbers[1:] if x <= pivot]
        greater = [x for x in numbers[1:] if x > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)

# Celery setup
app = celery.Celery('sort_algorithm',
                   broker='amqp://guest@localhost//',
                   backend='rpc://')

@app.task
def sort_numbers(numbers, algorithm='quick_sort'):
    # This function decides which sort algorithm to use based on the input parameter
    if algorithm == 'bubble_sort':
        return bubble_sort(numbers)
    elif algorithm == 'quick_sort':
        return quick_sort(numbers)
    else:
        raise ValueError("Invalid sorting algorithm specified")

def main():
    # Example usage of sorting task
    try:
        numbers = [64, 34, 25, 12, 22, 11, 90]
        result = sort_numbers(numbers, algorithm='quick_sort').get()
        print("Sorted numbers: ", result)
    except Exception as e:
        print("An error occurred: ", e)

if __name__ == '__main__':
    main()