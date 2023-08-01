from unittest import TestCase

# from git import objects

from .models import *


# class BookModelTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         language = Language.objects.create(language="Slovenský")
#         genre = Genre.objects.create(name="Detskáliteratúra")
#         author = Author.objects.create(
#             first_name="Jan",
#             last_name="Smrek",
#             birth_date="1898-12-16",
#
#             )
#         book=Book.objects.create(
#             name="Machule",
#             original_name="Machule",
#             year=1956,
#             description="Báseňjezoškolskéhoprostredia.OtomakosaškolákoviJankovispravívzošitemachuľa...",
#             language="Slovenský",
#             isbn=15
#
#             )
#
#     def test_name(self):
#         book=Book.objects.get(id=1)
#         self.assertEqual(book.name, "Machule")
#
#     def test_year(self):
#         book=Book.objects.get(id=1)
#         self.assertEqual(book.year, 1956)
#
#     def test_language_str(self):
#         language=Language.objects.get(id=1)
#         expected_str="Slovenský"
#         self.assertEqual(str(language),expected_str)
#         # self.assertEqual(language.__str__(),"Machule(1956)")

