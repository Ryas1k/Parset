import requests
from bs4 import BeautifulSoup

# URL-адрес страницы, которую будем парсить
url = "https://www.python.org/blogs/"  # Замените на URL реального сайта
# Заголовки, чтобы имитировать запрос из браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
print(f"Начинаем парсинг сайта: {url}")
# Отправляем GET-запрос на сайт и сохраняем ответ
# --- Шаг 2: Получение HTML-кода ---
try:
    # Отправляем GET-запрос на сайт
    response = requests.get(url, headers=headers, timeout=10)

    # --- Вот наша проверка ---
    # Если код состояния равен 200, то все хорошо
    if response.status_code == 200:
        print("Успех! Код состояния 200. Начинаем обработку HTML.")
        
        # --- Шаг 3: "Разбор" HTML ---
        # Теперь мы уверены, что в response.text есть валидный HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Шаг 4: Поиск нужных данных ---
        post_list_container = soup.find('ul', class_='list-recent-posts')

        if post_list_container:
            all_posts = post_list_container.find_all('li')
            print(f"\nНайдено {len(all_posts)} постов. Выводим результат:\n")
            
            with open('parset\posts.txt', 'w', encoding='utf-8') as files:
                # --- Шаг 5: Извлечение и вывод данных ---
                for post in all_posts:
                    link_tag = post.find('a')

                    if link_tag:
                        title = link_tag.text.strip()
                        full_link = 'https://www.python.org' + link_tag.get('href')
                        files.write(f"Заголовок: {title}\n")
                        files.write(f"Ссылка: {full_link}\n")
            print('Данные успешно записаны в файл -- posts.txt')   
                     
        else:
            print("Не удалось найти блок с постами на странице.")

    # Если код состояния не 200, сообщаем об ошибке
    else:
        print(f"Ошибка! Сайт ответил с кодом состояния: {response.status_code}")
        print(f"Причина: {response.reason}") # response.reason дает текстовое описание кода

# Обработка ошибок, если сайт вообще не ответил (например, нет интернета)
except requests.exceptions.RequestException as e:
    print(f"Ошибка! Не удалось подключиться к сайту: {e}")
