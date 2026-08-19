from book import Book
from typing import List, Optional, Dict
from datetime import datetime
import json


class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: List[Book] = []
        self.borrowed_books: Dict[int, str] = {}  # book_id -> user_name
        self.__opened_at = datetime.now()

    def add_book(self, book: Book) -> bool:
        """Добавляет книгу в библиотеку"""
        if any(b.id == book.id for b in self.books):
            return False
        self.books.append(book)
        return True

    def remove_book(self, book_id: int) -> bool:
        """Удаляет книгу из библиотеки"""
        for i, book in enumerate(self.books):
            if book.id == book_id:
                if book.is_available:
                    self.books.pop(i)
                    return True
                return False
        return False

    def find_book(self, **kwargs) -> List[Book]:
        """Поиск книг по различным критериям"""
        results = []
        for book in self.books:
            match = True
            for key, value in kwargs.items():
                if hasattr(book, key):
                    if getattr(book, key) != value:
                        match = False
                        break
            if match:
                results.append(book)
        return results

    def borrow_book(self, book_id: int, user_name: str) -> bool:
        """Выдает книгу пользователю"""
        for book in self.books:
            if book.id == book_id and book.is_available:
                book.is_available = False
                self.borrowed_books[book_id] = user_name
                return True
        return False

    def return_book(self, book_id: int) -> bool:
        """Возвращает книгу в библиотеку"""
        for book in self.books:
            if book.id == book_id and not book.is_available:
                book.is_available = True
                self.borrowed_books.pop(book_id, None)
                return True
        return False

    def get_statistics(self) -> Dict[str, any]:
        """Получает статистику библиотеки"""
        total = len(self.books)
        available = sum(1 for b in self.books if b.is_available)
        borrowed = total - available

        avg_rating = 0.0
        if total > 0:
            total_rating = sum(b.get_average_rating() for b in self.books)
            avg_rating = round(total_rating / total, 1)

        return {
            'total_books': total,
            'available': available,
            'borrowed': borrowed,
            'average_rating': avg_rating,
            'opened': self.__opened_at.strftime("%Y-%m-%d %H:%M")
        }