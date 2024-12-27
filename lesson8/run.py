import threading
import random
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

numbers = []
condition = threading.Condition()

def fill_list():
    global numbers
    with condition:
        logging.info("Thread T1: Filling the list with random numbers.")
        numbers = [random.randint(1, 1000) for _ in range(10_000)]
        logging.info("Thread T1: List filled.")
        condition.notify_all()

def calculate_sum():
    with condition:
        condition.wait() 
        total_sum = sum(numbers)
        logging.info(f"Thread T2: Sum of elements is {total_sum}.")

def calculate_average():
    with condition:
        condition.wait()
        average = sum(numbers) / len(numbers)
        logging.info(f"Thread T3: Arithmetic average is {average}.")

def get_primes_amount(nums):
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def count_primes(sublist, result, index):
        result[index] = sum(1 for x in sublist if is_prime(x))

    thread_count = min(len(nums), 4)  
    chunk_size = len(nums) // thread_count
    threads = []
    results = [0] * thread_count

    for i in range(thread_count):
        start = i * chunk_size
        end = None if i == thread_count - 1 else (i + 1) * chunk_size
        thread = threading.Thread(target=count_primes, args=(nums[start:end], results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)

if __name__ == "__main__":
    t1 = threading.Thread(target=fill_list)
    t2 = threading.Thread(target=calculate_sum)
    t3 = threading.Thread(target=calculate_average)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    test_numbers = [40000, 400, 1000000, 700]
    for number in test_numbers:
        primes_count = get_primes_amount(range(1, number + 1))
        logging.info(f"Number of primes up to {number}: {primes_count}")
