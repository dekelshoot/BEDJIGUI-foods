from django.contrib import admin
from project.models import Reservation, User, Menu,Cart_List,Commande
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'email', 'people', 'time', 'phone',
                    'date_reserved', 'status']
    
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'prix','picture']

class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'prix','picture']

class MyUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('picture','telephone','adresse')}),
    )
class CardAdmin(admin.ModelAdmin):
	model = Cart_List

class CommandeAdmin(admin.ModelAdmin):
	model = Commande
     
admin.site.register(User, MyUserAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Cart_List, CardAdmin)
admin.site.register(Commande, CommandeAdmin)