from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
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
    """Menu: Ce modèle représente un menu avec un nom,une image,un prix et une description optionnelle et un prix."""
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
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	cart_id = models.ManyToManyField(Cart_List)
	complete = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		if self.complete == False:
			return "Statut: en cours"
		else:
			return "Statut: Complete"

# class Commande(models.Model):
#     """
#     Commande : Ce modèle représente une commande avec une date et un total.
#     Le total peut être calculé automatiquement en fonction des Menus et des quantités associées.
#     """
#     date_commande = models.DateTimeField(auto_now_add=True)
#     total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f'Commande #{self.id} - {self.date_commande}'

# class CommandeProduit(models.Model):
#     """
#     CommandeProduit : C'est un modèle intermédiaire qui relie une commande à plusieurs Menus en 
#     spécifiant la quantité de chaque Menu dans la commande. Cela permet de gérer la relation 
#     plusieurs-à-plusieurs avec des attributs supplémentaires (comme la quantité).

#     """
#     commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     quantite = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f'{self.quantite} x {self.menu.name} dans {self.commande}'
class Reservation(models.Model):
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
