import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Загрузка ресурсов для NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Лемматизация текста
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words if word.isalnum()]
    return ' '.join(lemmatized_words)

# Очистка текста
def clean_text(text):
    text = text.lower()  # Приведение к нижнему регистру
    text = re.sub(r'\s+', ' ', text)  # Удаление лишних пробелов
    text = re.sub(r'[^\w\s]', '', text)  # Удаление знаков препинания
    return text

# Удаление повторяющихся слов
def remove_duplicates(text):
    words = text.split()
    seen = set()
    unique_words = []
    for word in words:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    return ' '.join(unique_words)

# Обработка данных для каждого URL
def process_item(item):
    combined_text = f"{item['title']} {item['meta_description']} {item['meta_keywords']} {item['headings']}"

    # Очистка текста
    cleaned_text = clean_text(combined_text)
    
    # Лемматизация текста
    lemmatized_text = lemmatize_text(cleaned_text)
    
    # Удаление повторяющихся слов
    unique_text = remove_duplicates(lemmatized_text)

    cleaned_text = remove_contacts(unique_text)
    
    return f"Сгенерируй объявление о {cleaned_text}"

def remove_contacts(text):
    # Шаблон для поиска номеров телефонов и адресов электронной почты
    pattern = r'\b\d{2}[-\s]?\d{2}[-\s]?\d{2}\b|\b\d{6}\b|[\w\.-]+@[\w\.-]+\.\w+\b'
    
    # Замена найденных совпадений на пустую строку
    clean_text = re.sub(pattern, '', text)

    # Удаление возможных оставшихся "Контактный телефон:" и "Email:" с любых следующих пробелов
    clean_text = re.sub(r'Контактный телефон:\s*|Email:\s*', '', clean_text)

    # Удаление лишних пробелов
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text

def remote_call():
    main()

# Основная функция
def main():
    # Считывание данных из JSON файла
    with open('parsed_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Обработка данных для каждого URL
    announcements = [process_item(item) for item in data]
    
    # Объединение объявлений в одну строку с разделением по строкам
    final_text = '\n'.join(announcements)
    
    # Запись результата в файл
    with open('announcement.txt', 'w', encoding='utf-8') as file:
        file.write(final_text)

    print("Объявления сгенерированы и сохранены в 'announcement.txt'.")

if __name__ == "__main__":
    main()
