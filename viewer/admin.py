from django.contrib import admin
from django import forms

from .models import *


class OrderItemInLine(admin.TabularInline):
	model = OrderItem
	extra = 0


class OrderAdmin(admin.ModelAdmin):
	inlines = [OrderItemInLine]

class AuthorForm(forms.ModelForm):
	birth_date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(format='%d.%m.%Y'), required=False)

	class Meta:
		model = Author
		fields = '__all__'
class AuthorModelAdmin(admin.ModelAdmin):
	form = AuthorForm


# Register your models here.
admin.site.register(Genre)
admin.site.register(Author, AuthorModelAdmin)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Rented)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Person)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Reserved)
