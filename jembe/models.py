from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Contact(models.Model):
    """
    Modèle pour stocker les informations de contact reçues via un formulaire de contact.
    """

    name = models.CharField(max_length=200)
    """
    Nom de la personne qui envoie le message.
    (Champ de type Char, longueur maximale 200 caractères)
    """

    email = models.EmailField()
    """
    Adresse e-mail de la personne qui envoie le message.
    (Champ de type EmailField, pour s'assurer qu'il s'agit d'une adresse e-mail valide)
    """

    phone = PhoneNumberField(blank=True)
    """
    Numéro de téléphone de la personne qui envoie le message (facultatif).
    (Champ de type PhoneNumberField, peut être vide)
    """

    subject = models.CharField(max_length=300)
    """
    Sujet du message.
    (Champ de type Char, longueur maximale 300 caractères)
    """

    message = models.TextField()
    """
    Contenu du message.
    (Champ de type TextField, pour un texte long)
    """

    date_sent = models.DateTimeField(auto_now_add=True)
    """
    Date et heure à laquelle le message a été envoyé.
    (Champ de type DateTimeField, généré automatiquement à chaque création de message)
    """

    def __str__(self):
        """
        Méthode pour définir la représentation textuelle de l'objet Contact.
        (Retourne l'adresse e-mail du contact)
        """
        return self.email

