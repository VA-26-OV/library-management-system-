import unittest
from book import Book
from library import Library
from book_manager import BookManager
import json
import tempfile
import os


class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        """Подготовка к каждому тесту"""
        self.library = Library("Test Library")
        self.book1 = Book(1, "1984", "George Orwell", 1949, "978-0451524935")
        self.book2 = Book(2, "Brave New World", "Aldous Huxley", 1932, "978-0060850524")
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.manager = BookManager(self.library)

    def test_book_creation(self):
        """Тест создания книги"""
        self.assertEqual(self.book1.title, "1984")
        self.assertEqual(self.book1.author, "George Orwell")
        self.assertTrue(self.book1.is_available)

    def test_add_rating(self):
        """Тест добавления оценок"""
        self.book1.add_rating(5)
        self.book1.add_rating(4)
        self.assertEqual(self.book1.get_average_rating(), 4.5)

        with self.assertRaises(ValueError):
            self.book1.add_rating(10)

    def test_borrow_book(self):
        """Тест выдачи книги"""
        self.assertTrue(self.library.borrow_book(1, "Иван"))
        self.assertFalse(self.book1.is_available)
        self.assertIn(1, self.library.borrowed_books)
        self.assertEqual(self.library.borrowed_books[1], "Иван")

        # Нельзя выдать уже занятую книгу
        self.assertFalse(self.library.borrow_book(1, "Петр"))

    def test_return_book(self):
        """Тест возврата книги"""
        self.library.borrow_book(1, "Иван")
        self.assertTrue(self.library.return_book(1))
        self.assertTrue(self.book1.is_available)
        self.assertNotIn(1, self.library.borrowed_books)

    def test_search_books(self):
        """Тест поиска книг"""
        results = self.manager.search_books("Orwell")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "1984")

    def test_statistics(self):
        """Тест статистики"""
        stats = self.library.get_statistics()
        self.assertEqual(stats['total_books'], 2)
        self.assertEqual(stats['available'], 2)
        self.assertEqual(stats['borrowed'], 0)

        self.library.borrow_book(1, "Иван")
        stats = self.library.get_statistics()
        self.assertEqual(stats['available'], 1)
        self.assertEqual(stats['borrowed'], 1)

    def test_export_import(self):
        """Тест экспорта/импорта"""
        # Экспорт
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_file = f.name

        try:
            self.manager.export_books_to_csv(csv_file)
            self.assertTrue(os.path.exists(csv_file))

            # Проверяем, что файл не пустой
            with open(csv_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertTrue(len(content) > 0)
        finally:
            os.unlink(csv_file)


if __name__ == '__main__':
    unittest.main()