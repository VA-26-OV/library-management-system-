from book import Book
from library import Library
from typing import List, Dict, Optional
import json
import csv
import os


class BookManager:
    def __init__(self, library: Library):
        self.library = library
        self.__operation_log: List[str] = []

    def add_book_from_json(self, json_file: str) -> int:
        """Добавляет книги из JSON файла"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            added = 0
            for item in data:
                if 'id' in item and 'title' in item and 'author' in item:
                    book = Book(
                        item['id'],
                        item['title'],
                        item['author'],
                        item.get('year', 0),
                        item.get('isbn', 'N/A')
                    )
                    if self.library.add_book(book):
                        added += 1
                        self.__log_operation(f"Добавлена книга: {book.title}")

            return added
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {json_file} не найден")
        except json.JSONDecodeError:
            raise ValueError("Неверный формат JSON")

    def export_books_to_csv(self, csv_file: str) -> bool:
        """Экспортирует информацию о книгах в CSV"""
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Название', 'Автор', 'Год', 'ISBN', 'Доступна', 'Рейтинг'])

                for book in self.library.books:
                    writer.writerow([
                        book.id,
                        book.title,
                        book.author,
                        book.year,
                        book.isbn,
                        'Да' if book.is_available else 'Нет',
                        book.get_average_rating()
                    ])
            self.__log_operation(f"Экспорт в CSV: {csv_file}")
            return True
        except Exception as e:
            raise RuntimeError(f"Ошибка при экспорте: {e}")

    def search_books(self, query: str) -> List[Dict[str, any]]:
        """Поиск книг по текстовому запросу"""
        results = []
        query_lower = query.lower()

        for book in self.library.books:
            if (query_lower in book.title.lower() or
                    query_lower in book.author.lower() or
                    query_lower in str(book.year)):
                results.append(book.get_info())

        self.__log_operation(f"Поиск: '{query}' найдено {len(results)} книг")
        return results

    def __log_operation(self, message: str) -> None:
        """Логирование операций"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__operation_log.append(f"[{timestamp}] {message}")

    def get_logs(self) -> List[str]:
        """Возвращает лог операций"""
        return self.__operation_log.copy()


```