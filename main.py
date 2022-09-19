# Лабораторная 1. Python 3.6+ (f-строки)
search_term = input('Enter search term: ').lower()

with open('books.csv', encoding='utf-8') as f:
    lines = f.read().split('\n')[1:-1]

long_name_counter = 0
bibliographic_links_count = 20
bibliographic_links = []
tags = set() # Множество обеспечивает отсутствие повторений
most_issued = []
search_results = []

for line in lines:
    # Парсинг CSV
    # ID;Название;Тип;Автор;Автор (ФИО);Возрастное ограничение на книгу;Дата поступления;Цена поступления;Кол-во выдач;Дата списания книги;Инвентарный номер;Выдана до;Жанр книги
    try:
        id, title, type, author, author_full_name, age_rating, receipt_date, price, issue_count, write_off_date, inventory_number, issue_term, genre = line.split(';')
    except:
        print(f'Incorrect record, ignoring. ID{id}') # Встречаются записи с ';' в названии
    # Подсчет количества записей, у которых в поле Название строка длиннее 30 символов
    if len(title) > 30:
        long_name_counter += 1
    # Поиск с фильтром по году получения (проверяет и псевдоним, и ФИО автора)
    if (search_term in author.lower() or search_term in author_full_name.lower()): # Вариант 5 - Без ограничений
        search_results.append(f'{author} - {title} ID{id}')
    # Генератор библиографических ссылок
    receipt_year = receipt_date.replace('.', ' ').split()[2]
    if bibliographic_links_count >= 0:
        bibliographic_links_count -= 1
        bibliographic_link = f'{author}. {title} - {receipt_year}'
        if not bibliographic_link in bibliographic_links: # Избавление от одинаковых записей
            bibliographic_links.append(bibliographic_link)
    # Допзадание - список тегов
    for tag in genre.split('#'):
        tags.add(tag.strip())
    # Допзадание - самые популярные книги
    most_issued.append((int(issue_count), author, title, id))
most_issued.sort(key=lambda x:x[0], reverse=True)

# Запись библиографических ссылок в файл
with open('links.txt', 'w', encoding='utf-8') as f:
    for i in range(len(bibliographic_links)):
        f.write(f'{i + 1}. {bibliographic_links[i]}\n')

print(f'Tags:{" #".join(tags)}') # Допзадание с длинным выводом
print(f'Number of records: {len(lines)}')
print(f'Records with name longer than 30 symbols: {long_name_counter}')
print('Bibliographic links generated and stored in links.txt')
print('Search results: ')
for i in search_results:
    print(f'    {i}')
print('Most-issued books:')
for i in most_issued[:20]:
    print(f'    {i[1]} - {i[2]} ID{i[3]}')