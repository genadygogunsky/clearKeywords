import re
from typing import List, Set

class KeywordCleaner:
    def __init__(self, minus_words_file: str = 'minus_words.txt'):
        """
        Инициализация класса очистки ключевых слов
        
        :param minus_words_file: путь к файлу с минус-словами
        """
        self.minus_words = self._load_minus_words(minus_words_file)

    def _load_minus_words(self, filepath: str) -> Set[str]:
        """
        Загрузка минус-слов из файла
        
        :param filepath: путь к файлу с минус-словами
        :return: множество минус-слов
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return {word.strip().lower() for word in file.readlines() if word.strip()}
        except FileNotFoundError:
            print(f"Файл {filepath} не найден. Используется пустой список минус-слов.")
            return set()

    def clean_keywords(self, input_file: str, output_file: str) -> None:
        """
        Очистка ключевых слов от минус-слов
        
        :param input_file: путь к входному файлу с ключевыми словами
        :param output_file: путь к выходному файлу с очищенными ключевыми словами
        """
        try:
            # Чтение входных ключевых слов
            with open(input_file, 'r', encoding='utf-8') as infile:
                keywords = [keyword.strip() for keyword in infile.readlines() if keyword.strip()]

            # Очистка ключевых слов
            cleaned_keywords = self._filter_keywords(keywords)

            # Сохранение очищенных ключевых слов
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for keyword in cleaned_keywords:
                    outfile.write(f"{keyword}\n")

            print(f"Очищено ключевых слов: {len(keywords)} → {len(cleaned_keywords)}")

        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

    def _filter_keywords(self, keywords: List[str]) -> List[str]:
        """
        Фильтрация ключевых слов
        
        :param keywords: список ключевых слов
        :return: очищенный список ключевых слов
        """
        cleaned_keywords = []

        for keyword in keywords:
            # Преобразование к нижнему регистру для сравнения
            lower_keyword = keyword.lower()
            
            # Проверка наличия минус-слов
            if not any(minus_word in lower_keyword for minus_word in self.minus_words):
                cleaned_keywords.append(keyword)

        return cleaned_keywords

    def interactive_mode(self):
        """
        Интерактивный режим для ручной очистки ключевых слов
        """
        print("Интерактивный режим очистки ключевых слов")
        print("Введите ключевые слова (для завершения введите пустую строку):")

        keywords = []
        while True:
            keyword = input("> ").strip()
            if not keyword:
            break
            keywords.append(keyword)

        print("\nМинус-слова для фильтрации:")
        print(", ".join(self.minus_words))

        cleaned_keywords = self._filter_keywords(keywords)

        print("\nОчищенные ключевые слова:")
        for keyword in cleaned_keywords:
            print(keyword)

def main():
    # Создание экземпляра класса KeywordCleaner
    cleaner = KeywordCleaner()

    # Выбор режима работы
    print("Выберите режим:")
    print("1. Очистка из файлов")
    print("2. Интерактивный режим")
    
    choice = input("Введите номер режима (1/2): ")

    if choice == '1':
        # Режим работы с файлами
        input_file = input("Введите путь к входному файлу с ключевыми словами: ")
        output_file = input("Введите путь к выходному файлу: ")
        
        cleaner.clean_keywords(input_file, output_file)
    
    elif choice == '2':
        # Интерактивный режим
        cleaner.interactive_mode()
    
    else:
        print("Некорректный выбор режима")

if __name__ == "__main__":
    main()
