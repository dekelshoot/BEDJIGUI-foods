from django import forms
from project.models import Reservation
from jembe.models import Contact
from project.models import User, Reservation



class ReservationForm(forms.ModelForm):
    """
    Formulaire de réservation basé sur le modèle Reservation.
    """

    date_reserved = forms.DateField(widget=forms.TextInput(attrs={}), required=True)
    """
    Champ "Date de réservation" utilisant un widget TextInput pour la saisie.
    Aucun attribut HTML supplémentaire n'est défini par défaut.
    Requis.
    """

    email = forms.EmailField(widget=forms.TextInput(attrs={'id': 'reservation_email'}))
    """
    Champ "Email" utilisant un widget TextInput pour la saisie.
    L'attribut HTML 'id' est défini à 'reservation_email' pour un meilleur ciblage CSS.
    """

    time = forms.TimeField(widget=forms.TextInput(attrs={'id': 'reservation_time', 'placeholder': "Heure prévue"}))
    """
    Champ "Heure" utilisant un widget TextInput pour la saisie.
    Les attributs HTML 'id' et 'placeholder' sont définis.
    'id' est défini à 'reservation_time' pour un meilleur ciblage CSS.
    'placeholder' affiche le texte "Heure prévue" pour guider l'utilisateur.
    """

    comment = forms.CharField(widget=forms.Textarea(attrs={'col': '30', 'rows': '10', 'placeholder': 'commentaire'}))
    """
    Champ "Commentaire" utilisant un widget Textarea pour la saisie de texte long.
    Les attributs HTML 'col', 'rows', et 'placeholder' sont définis.
    'col' définit le nombre de colonnes (30 ici).
    'rows' définit le nombre de lignes (10 ici) pour la zone de texte.
    'placeholder' affiche le texte "commentaire" pour guider l'utilisateur.
    """

    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+32', 'id': 'reservation_phone'}), required=True)
    """
    Champ "Téléphone" utilisant un widget TextInput pour la saisie.
    Les attributs HTML 'placeholder' et 'id' sont définis.
    'placeholder' affiche le texte "+32" pour suggérer le code de pays.
    'id' est défini à 'reservation_phone' pour un meilleur ciblage CSS.
    Requis.
    """

    first_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'reservation_phone'}), required=True)
    """
    Champ "Prénom" utilisant un widget TextInput pour la saisie.
    L'attribut HTML 'id' est défini à 'reservation_phone' (erreur probable, devrait être 'reservation_first_name').
    Requis.
    """

    class Meta:
        """
        Définition des métadonnées du formulaire.
        """
        model = Reservation  # Le formulaire est basé sur le modèle Reservation.
        fields = ['first_name', 'last_name', 'email', 'people', 'time', 'phone', 'date_reserved', 'status', 'comment']  # Champs à inclure dans le formulaire.
        exclude = ['last_name', 'status']  # Champs du modèle à exclure du formulaire (gérés ailleurs).



class RegisterForm(forms.ModelForm):
    """
    Formulaire d'inscription utilisateur, basé sur le modèle User de Django.
    """
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
    """
    Formulaire de connexion simple avec des champs nom d'utilisateur et mot de passe.
    """
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class ContactForm(forms.ModelForm):
    """
    Formulaire pour la soumission de contact utilisateur, basé sur le modèle Contact.

    Suppose que le modèle Contact existe dans la même application que ce formulaire.
    """
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
