from django.db.models import Count

from viewer.models import Book, Author, Reserved, Rented, Person


class StatisticMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.book_sum = Book.objects.count()
        request.author_sum = Author.objects.count()
        request.reserved_sum = Reserved.objects.count()
        request.rented_sum = Rented.objects.count()
        request.person_sum = Person.objects.count()

        response = self.get_response(request)
        return response


class MostRentedBooksMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.most_rented_books = Book.objects.annotate(num_rented=Count('rented')).order_by('-num_rented')[:5]
        response = self.get_response(request)
        return response







