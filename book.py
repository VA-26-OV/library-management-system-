from typing import List, Dict, Optional
from datetime import datetime
import json


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, isbn: str):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.is_available = True
        self.rating: List[int] = []
        self.__created_at = datetime.now()

    def get_info(self) -> Dict[str, any]:
        """Возвращает информацию о книге в виде словаря"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'isbn': self.isbn,
            'available': self.is_available,
            'rating': self.get_average_rating(),
            'created': self.__created_at.strftime("%Y-%m-%d")
        }

    def get_average_rating(self) -> float:
        """Возвращает среднюю оценку книги"""
        if not self.rating:
            return 0.0
        return round(sum(self.rating) / len(self.rating), 1)

    def add_rating(self, score: int) -> None:
        """Добавляет оценку книге (от 1 до 5)"""
        if 1 <= score <= 5:
            self.rating.append(score)
        else:
            raise ValueError("Рейтинг должен быть от 1 до 5")

    def __str__(self) -> str:
        status = "Доступна" if self.is_available else "Занята"
        return f"'{self.title}' by {self.author} ({self.year}) - {status}"


```
```bash