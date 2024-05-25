from django import forms
from project.models import Reservation
from jembe.models import Contact
from project.models import User, Reservation



class ReservationForm(forms.ModelForm):
    
    date_reserved = forms.DateField(widget=forms.TextInput(
        attrs={}), required=True,)
    email = forms.EmailField(widget=forms.TextInput
                             (attrs={'id': 'reservation_email'}))
    time = forms.TimeField(
        widget=forms.TextInput(attrs={'id': 'reservation_time',
                                      'placeholder': "Heure prévue"}))

    comment = forms.CharField(widget=forms.Textarea(
        attrs={'col': '30', 'rows': '10', 'placeholder': 'commentaire'}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': '+32',
               'id': 'reservation_phone',
               }), required=True,)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'reservation_phone',
               }), required=True,)
    
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name',
                  'email', 'people', 'time',
                  'phone', 'date_reserved', 'status', 'comment']
        exclude = ['last_name', 'status']

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'username'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email Adress'}))
    adresse = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'adresse'}))
    telephone = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'téléphone',
               'id': 'téléphone',
               }), required=True,)
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'picture', 'password','telephone','adresse']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
