from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from viewer.models import Person


# Create your views here.

class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)
        person = Person(user=user)
        if commit:
            person.save()
        return user


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def form_invalid(self, form):
        self.form = form
        return super().form_invalid(form)