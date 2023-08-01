import json
from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.transaction import atomic
from django.forms import ModelForm, ModelMultipleChoiceField
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from viewer.models import Book, Genre, Author, Language, Order, OrderItem, Person, Reserved, Rented, Rating, Comment
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
	return render(request, template_name="index.html")


def new_books(request):
	book_list = Book.objects.all().order_by('-id')
	genres_list = Genre.objects.all()
	context = {'books': book_list, 'genres': genres_list}
	return render(request, template_name='index.html', context=context)


def authors(request):
	author_list = Author.objects.all()
	paginator = Paginator(author_list, 15)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {'authors': page_obj}
	return render(request, template_name='authors.html', context=context)


def authors_ad(request):
	authors_list = Author.objects.all()
	context = {'authors': authors_list}
	return render(request, template_name='authors_ad.html', context=context)


def languages(request):
	languages_list = Language.objects.all()
	context = {'languages': languages_list}
	return render(request, template_name='languages.html', context=context)


def conditions(request):
	return render(request, template_name='conditions.html')


class BooksView(TemplateView):
	template_name = 'books.html'
	book_list = Book.objects.all().order_by('name')
	author_list = Author.objects.all()
	paginator = Paginator(book_list, 10)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page_number = self.request.GET.get('page')
		page_obj = self.paginator.get_page(page_number)
		context['books'] = page_obj
		context['authors'] = self.author_list
		return context


class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = '__all__'

	def clean_name(self):
		cleaned_data = super().clean()
		name = cleaned_data.get('name').strip()
		if len(name) < 3:
			raise ValidationError('Name should have minimum 3 letters')
		name = name.title()
		return name

	def clean_original_name(self):
		cleaned_data = super().clean()
		name = cleaned_data.get('original_name').strip()
		if len(name) < 3:
			raise ValidationError('Name should have minimum 3 letters')
		name = name.title()
		return name

	def clean_year(self):
		cleaned_data = super().clean()
		year = cleaned_data.get('year')
		if year:
			current_year = timezone.now().year

		if year < 1500 or year > current_year:
			raise ValidationError('Enter correct year')
		return year

	def clean_description(self):
		cleaned_data = super().clean()
		description = cleaned_data.get('description').strip()
		if len(description) < 20:
			raise ValidationError('Description should have minimum 20 letters')
		return description

	def clean_page(self):
		cleaned_data = super().clean()
		page = cleaned_data.get('page')
		if (page < 1 or page > 9999):
			raise ValidationError('Enter correct number of pages')
		return page


class LoginRequiredMixin:
	@classmethod
	def as_view(cls, **kwargs):
		view = super().as_view(**kwargs)
		return login_required(view)


class BookCreateView(LoginRequiredMixin, CreateView):
	template_name = 'new_book.html'
	form_class = BookForm
	success_url = reverse_lazy('home')


class BookUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'new_book.html'
	model = Book
	form_class = BookForm
	success_url = reverse_lazy('books')


class BookDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'book_delete_confirm.html'
	model = Book
	success_url = reverse_lazy('books')


def book(request, pk):
	book = Book.objects.get(id=pk)
	user = request.user

	if request.method == 'POST':
		person = Person.objects.get(user=request.user)
		new_comment = request.POST.get('comment')
		user_comment = Comment.objects.get_or_create(id_book=book, id_user=person)[0]
		user_comment.comment = new_comment
		user_comment.save()
	comments = Comment.objects.filter(id_book=book)
	# rating = Rating.objects.get(id_book=book, id_user=person)
	avg_rating = Rating.objects.filter(id_book=book).aggregate(Avg('rating'))
	if user.is_authenticated:
		person = Person.objects.get(user=request.user)
		rating = Rating.objects.filter(id_book=book, id_user=person)
		if rating:
			rating = Rating.objects.get(id_book=book, id_user=person)
			rating = rating.rating
		reserved = Reserved.objects.filter(id_book=book, id_user=person, email_sent=False)
		context = {'book': book, 'comments': comments, 'reserved': reserved, 'avg_rating': avg_rating['rating__avg'],
		           'rating': rating}
	else:
		context = {'book': book, 'comments': comments, 'avg_rating': avg_rating['rating__avg']}
	return render(request, template_name='book.html', context=context)


def rate_book(request, id_book, rating):
	book = Book.objects.get(pk=id_book)
	user = Person.objects.get(user=request.user)
	if Rating.objects.filter(id_book=book, id_user=user).count() > 0:
		user_rating = Rating.objects.get(id_book=book, id_user=user)
		user_rating.rating = rating
		user_rating.save()
		rating = user_rating.rating

	else:
		user_rating = Rating.objects.create(id_book=book, id_user=user, rating=rating)
		user_rating.save()
	comments = Comment.objects.filter(id_book=book)

	avg_rating = Rating.objects.filter(id_book=book).aggregate(Avg('rating'))
	context = {'book': book, 'rating': rating, 'avg_rating': avg_rating['rating__avg'], 'comments': comments}

	return render(request, template_name='book.html', context=context)


def delete_rating(request, id_book):
	book = Book.objects.get(pk=id_book)
	user = Person.objects.get(user=request.user)

	if Rating.objects.filter(id_book=book, id_user=user).count() > 0:
		user_rating = Rating.objects.get(id_book=book, id_user=user)
		user_rating.delete()
	rating = None

	comments = Comment.objects.filter(id_book=book)

	avg_rating = Rating.objects.filter(id_book=book).aggregate(Avg('rating'))

	context = {'book': book, 'rating': rating, 'avg_rating': avg_rating['rating__avg'], 'comments': comments}

	return render(request, template_name='book.html', context=context)


def delete_comment(request, id_book, id_user):
	book = Book.objects.get(id=id_book)
	user = Person.objects.get(user=id_user)

	if Comment.objects.filter(id_book=book, id_user=user).count() > 0:
		user_comment = Comment.objects.get(id_book=book, id_user=user)
		user_comment.delete()

	comments = Comment.objects.filter(id_book=book)

	rating = None

	if user.user.is_authenticated and Rating.objects.filter(id_book=book, id_user=user).count() > 0:
		rating = Rating.objects.get(id_book=book, id_user=user)
	avg_rating = Rating.objects.filter(id_book=book).aggregate(Avg('rating'))
	context = {'book': book, 'rating': rating, 'avg_rating': avg_rating['rating__avg'], 'comments': comments}

	return render(request, template_name='book.html', context=context)


class UsersView(TemplateView):
	template_name = 'users.html'
	users_list = Person.objects.all().order_by('-id')
	paginator = Paginator(users_list, 10)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page_number = self.request.GET.get('page')
		page_obj = self.paginator.get_page(page_number)
		context['users'] = page_obj
		return context


def user_page(request, pk):
	user = Person.objects.get(id=pk)
	orders = Order.objects.filter(user=user, complete=True ).order_by('-id')
	context = {'user': user, 'orders': orders}
	return render(request, template_name='user.html', context=context)


def user_booked(request, pk):
	user = Person.objects.get(id=pk)
	orders = Order.objects.filter(user=user).order_by('-id')

	context = {'user': user, 'orders': orders}
	return render(request, template_name='user_booked.html', context=context)


def author(request, pk):
	author = Author.objects.get(id=pk)
	writing = Book.objects.filter(author=author)
	context = {'author': author, 'writing': writing}
	return render(request, template_name='author.html', context=context)


class AuthorForm(ModelForm):
	class Meta:
		model = Author
		fields = '__all__'

	def clean_name(self):
		cleaned_data = super().clean()
		name = cleaned_data.get('name')
		if not name.replace(" ", "").isalpha():
			raise ValidationError('Enter correct name')
		return name

	def clean_birth_date(self):
		cleaned_data = super().clean()
		birth_date = cleaned_data.get('birth_date')
		if birth_date:
			birth_year = birth_date.year
			current_date = timezone.now().date()
			current_year = timezone.now().year
			if birth_year < 1500 or birth_year > current_year:
				raise ValidationError('Invalid year of birth')
			if birth_date > current_date:
				raise ValidationError('Date cannot be in the future')
		return birth_date


class AuthorCreateView(LoginRequiredMixin, CreateView):
	template_name = 'new_author.html'
	form_class = AuthorForm
	success_url = reverse_lazy('authors_ad')


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'new_author.html'
	model = Author
	form_class = AuthorForm
	success_url = reverse_lazy('authors_ad')


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'author_delete_confirm.html'
	model = Author
	success_url = reverse_lazy('authors_ad')


def genres(request):
	genres_list = Genre.objects.all()
	paginator = Paginator(genres_list, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {'genres': page_obj}
	return render(request, template_name='genres.html', context=context)


def genre(request, pk):
	books = Book.objects.filter(genre=pk).order_by('name')
	paginator = Paginator(books, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {'books': page_obj}
	return render(request, template_name='genre.html', context=context)


class GenreForm(ModelForm):
	class Meta:
		model = Genre
		fields = '__all__'

	def clean_name(self):
		cleaned_data = super().clean()
		name = cleaned_data.get('name').strip()
		allowed = ["sci-fi"]
		if len(name) < 3:
			raise ValidationError('Genre should have minimum 3 letters')
		if not (name.replace(" ", "").isalpha() or name.lower() in allowed):
			raise ValidationError('Enter correct genre')
		name = name.title()
		return name


class GenreCreateView(LoginRequiredMixin, CreateView):
	template_name = 'new_genre.html'
	form_class = GenreForm
	success_url = reverse_lazy('genres')


class GenreUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'new_genre.html'
	model = Genre
	form_class = GenreForm
	success_url = reverse_lazy('genres')


class GenreDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'genre_delete_confirm.html'
	model = Genre
	success_url = reverse_lazy('genres')


class LanguageForm(ModelForm):
	class Meta:
		model = Language
		fields = '__all__'

	def clean_language(self):
		cleaned_data = super().clean()
		language = cleaned_data.get('language').strip()
		if not language.replace(" ", "").isalpha():
			raise ValidationError('Enter correct language')
		if len(language) < 2:
			raise ValidationError('Language should have minimum 2 letters')
		language = language.title()
		return language


class LanguageCreateView(LoginRequiredMixin, CreateView):
	template_name = 'new_language.html'
	form_class = LanguageForm
	success_url = reverse_lazy('languages')


class LanguageUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'new_language.html'
	model = Language
	form_class = LanguageForm
	success_url = reverse_lazy('languages')


class LanguageDeleteView(LoginRequiredMixin, DeleteView):
	template_name = 'language_delete_confirm.html'
	model = Language
	success_url = reverse_lazy('genres')


def search(request):
	if request.method == 'POST':
		pattern = request.POST.get('editbox_search').strip()
		if len(pattern) > 0:
			books_name = Book.objects.filter(name__contains=pattern)
			books_original_name = Book.objects.filter(original_name__contains=pattern)
			books_description = Book.objects.filter(description__contains=pattern)
			authors = Author.objects.filter(name__contains=pattern)
			genres = Genre.objects.filter(name__contains=pattern)
			users = Person.objects.filter(user__first_name__icontains=pattern) \
			        or Person.objects.filter(user__last_name__icontains=pattern) \
			        or Person.objects.filter(user__username__icontains=pattern)
			persons = Person.objects.filter()
			context = {'pattern': pattern,
			           'books_name': books_name,
			           'books_original_name': books_original_name,
			           'books_description': books_description,
			           'authors': authors,
			           'genres': genres,
			           'users': users}
			return render(request, template_name='search.html', context=context)
	return render(request, 'index.html')


def cart(request):
	if request.user.is_authenticated:
		customer = request.user.person
		order, created = Order.objects.get_or_create(user=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_items': 0}
	context = {'items': items, 'order': order}
	return render(request, 'cart.html', context)


@atomic
def update_item(request):
	data = json.loads(request.body)
	book_id = data['book_id']
	action = data['action']
	# person = data['person']

	customer = request.user.person
	book = Book.objects.get(id=book_id)
	order, created = Order.objects.get_or_create(user=customer, complete=False)

	if action == 'add':
		if book.amount > 0:
			if not OrderItem.objects.filter(cart=order, book=book).exists():
				order_item, created = OrderItem.objects.get_or_create(cart=order, book=book)
			order_item.save()
			book.amount -= 1
			book.save()
	if action == 'remove':
		order_item = OrderItem.objects.get(cart=order, book=book)
		order_item.delete()
		book.amount += 1
		book.save()
	if action == "reserve":
		reserve = Reserved.objects.create(id_user=customer, id_book=book)
		reserve.save

	return JsonResponse('Item was added', safe=False)


@atomic
def order_done(request):
	customer = request.user.person
	order, created = Order.objects.get_or_create(user=customer, complete=False)
	orderitems = order.orderitem_set.all()
	order.complete = True
	order.save()
	for orderitem in orderitems:
		rented = Rented.objects.create(id_book=orderitem.book, id_user=customer, id_order=order)
		rented.save()
	return render(request, template_name="order_done.html")


def booked(request):
	rented_books = Rented.objects.all().order_by('-id')

	context = {'rented_books': rented_books}
	return render(request, template_name="booked.html", context=context)


def reservations(request, pk):
	user = Person.objects.get(id=pk)
	reservations = Reserved.objects.filter(id_user=user).order_by('-id')
	context = {'user': user, 'reservations': reservations}
	return render(request, template_name='reservations.html', context=context)


@atomic
def change_booked(request):
	data = json.loads(request.body)
	book_id = data['book_id']
	order_id = data['order_id']

	action = data['action']
	customer = data['person']
	book = Book.objects.get(id=book_id)
	order = Order.objects.get(id=order_id)
	orderitem = OrderItem.objects.get(cart=order_id, book=book)
	rented = Rented.objects.get(id_order=order_id, id_book=book, id_user=customer)

	if action == 'cancel':
		rented.canceled = True
		rented.save()
		orderitem.canceled = True
		orderitem.save()
		book.amount += 1
		book.save()
	if action == 'rent':
		rented.rent_date = datetime.now()
		rented.return_to_date = datetime.now() + timedelta(days=28)
		rented.save()
	if action == 'return':
		rented.return_date = datetime.now()
		rented.save()
		book.amount += 1
		book.save()
	if action == 'extend':
		rented.return_to_date += timedelta(days=7)
		rented.extend = True
		rented.save()

	return JsonResponse('Item was changed', safe=False)


def change_membership(request):
	data = json.loads(request.body)
	user_id = data['user_id']
	user = Person.objects.get(user=user_id)
	if user.pay_to:
		user.pay_to = user.pay_to + timedelta(days=365)
		user.save()
	else:
		user.pay_to = datetime.now() + timedelta(days=365)
		user.save()
	return JsonResponse('Item was changed', safe=False)


def change_reservation(request):
	data = json.loads(request.body)
	user_id = data['person']
	book_id = data['book_id']
	reservation = Reserved.objects.get(id_book=book_id, id_user=user_id, email_sent=False, canceled=False)
	reservation.canceled = True
	reservation.save()
	return JsonResponse('Item was changed', safe=False)
