from django import forms
from project.models import User, Reservation,Menu


class MenuForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'nom', 'class': "form-control"}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'description', 'class': "form-control"}))
    prix = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'prix', 'class': "form-control"}))
    
    class Meta:
        model = Menu
        fields = ['name', 'description', 'prix','picture']

class MenuForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'nom', 'class': "form-control"}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'description', 'class': "form-control"}))
    prix = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'prix', 'class': "form-control"}))
    
    class Meta:
        model = Menu
        fields = ['name', 'description', 'prix','picture']
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': "form-control"}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First name', 'class': "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last name' ,'class': "form-control"}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'username','class': "form-control"}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email Adress','class': "form-control"}))
    adresse = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'adresse','class': "form-control"}))
    telephone = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': '+32','class': "form-control"}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password','telephone','adresse']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class UpdateUser(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'picture', 'bio',
                  'phone_number', 'email', 'website']


class ReservationForm(forms.ModelForm):
    time = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'timepicker',
                                      'class': 'input-group'}))
    date_reserved = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': 'mm-dd-yyyy',
               'id': 'datepicker'}), required=True,)

    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name',
                  'email', 'people', 'time',
                  'phone', 'date_reserved', 'status']
