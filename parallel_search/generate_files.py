import os
import random
import string

def generate_random_words(num_words, keywords):
    words = []
    for _ in range(num_words):
        if random.random() < 0.1:  # 10% шанс вставити ключове слово
            words.append(random.choice(keywords))
        else:
            word_length = random.randint(3, 10)
            word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
            words.append(word)
    return words

def generate_files(num_files, dir_path, keywords):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for i in range(1, num_files + 1):
        file_name = f'file{i}.txt'
        file_path = os.path.join(dir_path, file_name)
        num_words = random.randint(100, 1000)
        words = generate_random_words(num_words, keywords)
        content = ' '.join(words)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    print(f'{num_files} файлів створено у директорії "{dir_path}".')

if __name__ == '__main__':
    # Кількість файлів для генерації
    num_files = 100  # Можете змінити за потребою

    # Шлях до директорії для збереження файлів
    dir_path = 'texts'

    # Автоматично генеруємо ключові слова
    keywords = [''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(10)]
    print(f'Згенеровані ключові слова: {keywords}')

    generate_files(num_files, dir_path, keywords)
