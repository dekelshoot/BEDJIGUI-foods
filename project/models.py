from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
    """
	Cette classe hérite de `AbstractUser` et décrit les utilisateurs du système avec des champs supplémentaires.

    Champs hérités :
    - `password` : Mot de passe de l'utilisateur.
    - `last_login` : Dernière connexion de l'utilisateur.
    - `is_superuser` : Indique si l'utilisateur a tous les droits.
    - `is_staff` : Indique si l'utilisateur peut accéder à l'interface d'administration.
    - `is_active` : Indique si l'utilisateur est actif.
    - `date_joined` : Date d'inscription de l'utilisateur.
    - `groups` : Groupes auxquels l'utilisateur appartient.
    - `user_permissions` : Permissions spécifiques de l'utilisateur.

    Champs personnalisés :
    - `first_name` (CharField) : Prénom de l'utilisateur. Longueur maximale de 50 caractères.
    - `last_name` (CharField) : Nom de famille de l'utilisateur. Longueur maximale de 50 caractères.
    - `username` (CharField) : Nom d'utilisateur unique. Longueur maximale de 50 caractères.
    - `email` (EmailField) : Adresse email de l'utilisateur.
    - `adresse` (CharField) : Adresse postale de l'utilisateur. Longueur maximale de 50 caractères.
    - `phone_number` (CharField) : Numéro de téléphone principal de l'utilisateur. Longueur maximale de 12 caractères.
    - `telephone` (CharField) : Numéro de téléphone secondaire de l'utilisateur. Longueur maximale de 30 caractères.
    - `picture` (ImageField) : Image de profil de l'utilisateur. Les images sont téléchargées dans le répertoire "media/picture".
    - `bio` (CharField) : Biographie de l'utilisateur. Longueur maximale de 300 caractères.
    - `website` (URLField) : Site web de l'utilisateur. Ce champ est facultatif (blank=True).

    Méthodes héritées :
    - `get_full_name()`: Retourne le nom complet de l'utilisateur.
    - `get_short_name()`: Retourne le prénom de l'utilisateur.
    - `email_user(subject, message, from_email=None, **kwargs)`: Envoie un email à l'utilisateur.

	
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField()
    adresse = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    telephone = models.CharField(max_length=30)
    picture = models.ImageField(upload_to="media/picture")

    bio = models.CharField(max_length=300)
    website = models.URLField(blank=True)
class Menu(models.Model):
    """
	Menu: Ce modèle représente un menu avec un nom,une image,un prix et une description optionnelle et un prix.
	 Champs :
    - `name` (CharField) : Nom du menu. Longueur maximale de 200 caractères.
    - `picture` (ImageField) : Image associée au menu. Les images sont téléchargées dans le répertoire "media/menu".
    - `description` (TextField) : Description optionnelle du menu. Ce champ peut être vide (blank=True) ou nul (null=True).
    - `prix` (DecimalField) : Prix du menu. Nombre maximum de chiffres : 10, dont 2 chiffres après la virgule.

    Méthodes :
    - `__str__()` : Retourne le nom du menu.
	"""
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="media/menu")
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Cart_List(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
	calculated_price = models.FloatField()
	is_current = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
			return f"{self.menu_id.name}, - prix: € {self.calculated_price}"
	

class Commande(models.Model):
	"""
    Cart_List: Ce modèle représente une liste de menus dans un panier d'achat pour un utilisateur spécifique.

    Champs :
    - `user_id` (ForeignKey) : Référence à l'utilisateur associé à ce panier. Clé étrangère pointant vers le modèle User. 
      Suppression en cascade en cas de suppression de l'utilisateur.
    - `menu_id` (ForeignKey) : Référence au menu associé à ce panier. Clé étrangère pointant vers le modèle Menu.
      Suppression en cascade en cas de suppression du menu.
    - `calculated_price` (FloatField) : Prix calculé du menu dans le panier.
    - `is_current` (BooleanField) : Indique si le panier est en cours. Défaut à True.
    - `created_at` (DateTimeField) : Date et heure de création du panier. Défini automatiquement à la création.

    Méthodes :
    - `__str__()` : Retourne une représentation en chaîne de caractères du panier sous la forme "nom du menu - prix: € prix calculé".
    """
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	cart_id = models.ManyToManyField(Cart_List)
	complete = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		if self.complete == False:
			return "Statut: en cours"
		else:
			return "Statut: Complete"


class Reservation(models.Model):
    """
    Reservation: Ce modèle représente une réservation avec les informations du client, le nombre de personnes, 
    la date et l'heure de la réservation, ainsi que le statut et un commentaire optionnel.

    Champs :
    - `first_name` (CharField) : Prénom du client. Longueur maximale de 200 caractères.
    - `last_name` (CharField) : Nom de famille du client. Longueur maximale de 200 caractères.
    - `email` (EmailField) : Adresse email du client.
    - `phone` (PhoneNumberField) : Numéro de téléphone du client. Ce champ peut être vide (blank=True).
    - `people` (CharField) : Nombre de personnes pour la réservation. Choix limités à des valeurs prédéfinies (1 à 5).
    - `time` (TimeField) : Heure de la réservation.
    - `date_reserved` (DateField) : Date de la réservation.
    - `date_booked` (DateTimeField) : Date et heure de l'enregistrement de la réservation. Définie automatiquement à la création.
    - `status` (CharField) : Statut de la réservation (pending ou confirmed). Défaut à pending.
    - `comment` (TextField) : Commentaire optionnel sur la réservation. Ce champ peut être vide (blank=True).

    Méthodes :
    - `__str__()` : Retourne le prénom du client associé à la réservation.
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True)
    one = '1'
    two = '2'
    three = '3'
    four = '4'
    five = '5'
    people_choices = (
        (one, 'une personne'), (two, 'deux personnes'),
        (three, 'trois personnes'), (four, 'quatre personnes'), (five, 'cinq personnes')
    )
    people = models.CharField(
        max_length=1, choices=people_choices, default=one)
    time = models.TimeField()
    date_reserved = models.DateField()
    date_booked = models.DateTimeField(auto_now_add=True)
    pending = "pending"
    confirmed = "confirmed"
    status_choices = ((pending, "pending"), (confirmed, "confirmed"))
    status = models.CharField(
        max_length=10, choices=status_choices, default=pending)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.first_name
