from django import forms
from project.models import User, Reservation,Menu


class MenuForm(forms.ModelForm):
    """
    MenuForm: Ce formulaire est utilisé pour créer et mettre à jour des instances du modèle Menu.

    Champs :
    - `name` (CharField) : Champ de texte pour le nom du menu avec un widget `TextInput` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.
    - `description` (CharField) : Champ de texte pour la description du menu avec un widget `Textarea` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.
    - `prix` (DecimalField) : Champ numérique pour le prix du menu avec un widget `NumberInput` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.
    - `picture` (ImageField) : Champ pour télécharger une image associée au menu. Ce champ est directement lié au modèle et n'a pas de widget personnalisé ici.

    Meta :
    - `model` : Indique que ce formulaire est lié au modèle `Menu`.
    - `fields` : Liste des champs du modèle `Menu` qui seront inclus dans le formulaire.
    """
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
    """
    RegisterForm: Ce formulaire est utilisé pour enregistrer un nouvel utilisateur avec les champs nécessaires.

    Champs :
    - `password` (CharField) : Champ de mot de passe avec un widget `PasswordInput` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.
    - `first_name` (CharField) : Champ de texte pour le prénom avec un widget `TextInput` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.
    - `last_name` (CharField) : Champ de texte pour le nom de famille avec un widget `TextInput` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.
    - `username` (CharField) : Champ de texte pour le nom d'utilisateur avec un widget `TextInput` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.
    - `email` (EmailField) : Champ de texte pour l'adresse email avec un widget `TextInput` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.
    - `adresse` (CharField) : Champ de texte pour l'adresse avec un widget `TextInput` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.
    - `telephone` (CharField) : Champ de texte pour le numéro de téléphone avec un widget `TextInput` personnalisé. 
      Le widget a des attributs supplémentaires pour le placeholder et la classe CSS.

    Meta :
    - `model` : Indique que ce formulaire est lié au modèle `User`.
    - `fields` : Liste des champs du modèle `User` qui seront inclus dans le formulaire.
    """
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
    """
    LoginForm: Ce formulaire est utilisé pour l'authentification des utilisateurs.

    Champs :
    - `username` (CharField) : Champ de texte pour le nom d'utilisateur avec un widget `TextInput`.
    - `password` (CharField) : Champ de mot de passe avec un widget `PasswordInput`.
    """
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class UpdateUser(forms.ModelForm):
    """
    UpdateUser: Ce formulaire est utilisé pour mettre à jour les informations de l'utilisateur.

    Meta :
    - `model` : Indique que ce formulaire est lié au modèle `User`.
    - `fields` : Liste des champs du modèle `User` qui seront inclus dans le formulaire.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'picture', 'bio',
                  'phone_number', 'email', 'website']


class ReservationForm(forms.ModelForm):
    """
    ReservationForm: Ce formulaire est utilisé pour créer et mettre à jour des instances du modèle Reservation.

    Champs personnalisés :
    - `time` (CharField) : Champ de texte pour l'heure de la réservation avec un widget `TextInput` personnalisé.
    - `date_reserved` (DateField) : Champ de date pour la date de réservation avec un widget `TextInput` personnalisé.

    Meta :
    - `model` : Indique que ce formulaire est lié au modèle `Reservation`.
    - `fields` : Liste des champs du modèle `Reservation` qui seront inclus dans le formulaire.
    """
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
