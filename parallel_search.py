import os
import threading
import multiprocessing
import time

def search_in_files(file_list, keywords, results, lock):
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        with lock:
                            if keyword not in results:
                                results[keyword] = []
                            results[keyword].append(file_path)
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")

def search_in_files_process(file_list, keywords, queue):
    process_results = {}
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        if keyword not in process_results:
                            process_results[keyword] = []
                        process_results[keyword].append(file_path)
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")
    queue.put(process_results)

def main_threading(keywords):
    start_time = time.time()

    dir_path = 'texts'
    all_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.txt')]

    num_threads = 4  # Можна змінити кількість потоків
    files_per_thread = len(all_files) // num_threads
    threads = []
    results = {}
    lock = threading.Lock()

    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = (i + 1) * files_per_thread if i != num_threads - 1 else len(all_files)
        file_subset = all_files[start_index:end_index]

        t = threading.Thread(target=search_in_files, args=(file_subset, keywords, results, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    print(f"Час виконання (threading): {end_time - start_time:.4f} секунд")
    print("Результати пошуку:")
    print(results)

def main_multiprocessing(keywords):
    start_time = time.time()

    dir_path = 'texts'
    all_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.txt')]

    num_processes = 4  # Можна змінити кількість процесів
    files_per_process = len(all_files) // num_processes
    processes = []
    queue = multiprocessing.Queue()

    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = (i + 1) * files_per_process if i != num_processes - 1 else len(all_files)
        file_subset = all_files[start_index:end_index]

        p = multiprocessing.Process(target=search_in_files_process, args=(file_subset, keywords, queue))
        processes.append(p)
        p.start()

    results = {}
    for _ in processes:
        process_result = queue.get()
        for keyword, files in process_result.items():
            if keyword not in results:
                results[keyword] = []
            results[keyword].extend(files)

    for p in processes:
        p.join()

    end_time = time.time()
    print(f"Час виконання (multiprocessing): {end_time - start_time:.4f} секунд")
    print("Результати пошуку:")
    print(results)

if __name__ == '__main__':
    # Згенеровані ключові слова 
    keywords = ['jpufw', 'btzvn', 'dmxnt', 'afgaf', 'jejjm', 'onwfb', 'bixcl', 'yogpu', 'zixrd', 'yrsht']

    print("Виберіть версію для запуску:")
    print("1. Багатопотокова версія")
    print("2. Багатопроцесорна версія")
    choice = input("Ваш вибір: ")

    if choice == '1':
        main_threading(keywords)
    elif choice == '2':
        main_multiprocessing(keywords)
    else:
        print("Невірний вибір.")
